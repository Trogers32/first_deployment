from django.shortcuts import render, redirect
from django.contrib import messages
from apps.login_registration.models import *
import datetime
import bcrypt
from django.core.urlresolvers import reverse
from django import template


def home(request):
    try:
        uid = int(request.session['user_id'])
        context = {
            "user" : User.objects.get(id=uid),
            "reviews" : Review.objects.all().order_by("-created_at")[:3],
            "other_reviews" : Review.objects.all().order_by("-created_at")[3:],
        }
        return render(request, "books/index.html", context)
    except:
        return redirect("/")

def add(request):
    try:
        uid = int(request.session['user_id'])
        context = {
            "user" : User.objects.get(id=uid),
            "authors" : Author.objects.all(),
        }
        return render(request, "books/addBook.html", context)
    except:
        return redirect("/")

def user(request, num):
# try:
    uid = int(request.session['user_id'])
    uid = User.objects.get(id=uid)
    context = {
        "user" : User.objects.get(id=num),
        "reviews" : Review.objects.filter(reviewer=uid),
        "lr" : len(Review.objects.filter(reviewer=uid)),
    }
    return render(request, "books/user.html", context)
# except:
    return redirect("/")

def book(request, num):
# try:
    uid = int(request.session['user_id'])
    bid = Book.objects.get(id=num)
    context = {
        "user" : User.objects.get(id=num),
        "reviews" : Review.objects.filter(book=bid),
        "book" : bid,
    }
    return render(request, "books/desc.html", context)
# except:
    return redirect("/")

def add_book(request):
    try:
        uid = int(request.session['user_id'])
        uid = User.objects.get(id=uid)
        if request.POST['new_auth'] == '':
            # create book
            # create review
            title = request.POST['title']
            author = request.POST['author']
            author = Author.objects.filter(name=author).first()
            Book.objects.create(title=title, author=author)
            book = Book.objects.filter(title=title).first()
            rev = Review.objects.create(reviewer=uid, book=book, rating=request.POST['rating'], content=request.POST['review'])
            return redirect('/books')
        else:
            # create author
            # create book
            # create review
            title = request.POST['title']
            author = request.POST['new_auth']
            author = Author.objects.create(name=author)
            book = Book.objects.create(title=title, author=author)
            rev = Review.objects.create(reviewer=uid, book=book, rating=request.POST['rating'], content=request.POST['review'])
            return redirect('/books')
    except:
        redirect('/')







def add_favorite(request, num):
    try:
        uid = int(request.session['user_id'])
        book = Book.objects.get(id=num)
        user = User.objects.get(id=uid)
        user.favorite_books.add(book)
        return redirect('/books')
    except:
        return redirect('/login')

def book_page(request, num):
# try:
    uid = int(request.session['user_id'])
    context = {
        "user" : User.objects.get(id=uid),
        "book" : Book.objects.get(id=num),
    }
    return render(request, 'books/desc.html', context)
# except:
    return redirect('/login')

def update(request, num):
    try:
        errors = Book.objects.book_validator(request.POST)
            # check if the errors dictionary has anything in it
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f"/books/{num}")
        else:
            uid = int(request.session['user_id'])
            Book.objects.filter(id=num).update(title=request.POST['title'], desc=request.POST['description'])
            return redirect(f"/books/{num}")
    except:
        return redirect('/login')

def delete(request, num):
# try:
    uid = int(request.session['user_id'])
    Book.objects.get(id=num).delete()
    return redirect("/books")
# except:
    return redirect('/login')

def fadd(request, num):
    try:
        uid = int(request.session['user_id'])
        book = Book.objects.get(id=num)
        user = User.objects.get(id=uid)
        user.favorite_books.add(book)
        return redirect(f'/books/{num}')
    except:
        return redirect('/login')

def remove_favorite(request, num):
# try:
    uid = int(request.session['user_id'])
    book = Book.objects.get(id=num)
    User.objects.get(id=uid).favorite_books.remove(book)
    return redirect(f"/books/{num}")
# except:
    return redirect('/login')