from __future__ import unicode_literals
from django.db import models
from datetime import datetime, timedelta
import bcrypt
import pytz
from validate_email import validate_email
import re


class User_validation(models.Manager):   
    def register_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['name']) < 2:
            errors["name"] = "First name should be at least 2 characters long."
        if len(postData['alias']) < 3:
            errors["alias"] = "Last name should be at least 2 characters long."
        if User.objects.filter(email=postData['email']).first():
            errors["email"] = "Email already registered."
        elif postData['email'] == '':
            errors["email"] = "Email can't be blank."
        else:
            is_valid = validate_email(postData['email'])
            if is_valid == False:
                errors["email"] = "Invalid email."
            elif not re.match(r"[^@]+@[^@]+\.[^@]+",postData['email']):
                errors["email"] = "Invalid email."
        if len(postData['password']) < 8:
            errors["password"] = "Password needs to be at least 8 characters long."
        elif postData['password'] != postData['confirm_password']:
            errors["password"] = "Passwords do not match."
        return errors

    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['email'])
        if user:
            logged_user = user[0] 
            if not bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()):
                errors['pword'] = "Incorrect email or password."
        else:
            errors['pword'] = "Incorrect email or password."
        return errors

class Book_validation(models.Manager):   
    def book_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['review']) < 5:
            errors["desc"] = "Review needs at least 5 characters."
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = User_validation()

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Book_validation()

class Review(models.Model):
    reviewer = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name="book_reviews", on_delete=models.CASCADE)
    rating = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)