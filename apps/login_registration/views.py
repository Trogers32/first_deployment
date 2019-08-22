from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import datetime
import bcrypt
from django.core.urlresolvers import reverse

###########################################################
###########################################################
        # methods for login and registration
###########################################################
###########################################################
def home(request):
    return render(request, "main/lr.html")

def success(request):
    try:
        uid = int(request.session['user_id'])
        context = {
            "user" : User.objects.get(id=uid),
        }
        return redirect("/books")
    except:
        return render(request, "main/FAIL.html")

def fail(request):
    return render(request, "main/FAIL.html")

def register(request):
    errors = User.objects.register_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/login")
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())  # create the hash     
        # make sure you put the hashed password in the database, not the one from the form!
        User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=pw_hash) 
        e = request.POST['email']
        user = User.objects.filter(email=e)
        logged_user = user[0]
        request.session['user_id'] = logged_user.id
    return redirect("/login/success")

def login(request):
    errors = User.objects.login_validator(request.POST)
    user = User.objects.filter(email=request.POST['email'])
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/login")
    if user:
        logged_user = user[0] 
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect("/login/success")
    return redirect('/login')

def logout(request):
    request.session.clear()
    return redirect("/login")

###########################################################
###########################################################
###########################################################