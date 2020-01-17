from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 1:
            errors['first_name'] = "Maybe you can do better than this?"
        if len(postData['last_name']) < 1:
            errors['last_name'] = "Perhaps have a better last name?"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Is this best you got?"
        user = User.objects.filter(email=postData['email'])
        if user:
           errors['email'] = "Entered email is already registered" 
        if len(postData['password']) < 7:
            errors['password'] = "You think you don't have a password?"
        if postData['password'] != postData['confirm_password']:
            errors['password'] = "Passwords do not match!"
        return errors

    def login_validator(self, postData):
        errors = {}
        # validating user by their e-mail when log-in
        # if no email was entered, cannot login
        if not EMAIL_REGEX.match(postData['email']):
            errors['wrong_email_format'] = "Follow the email format!"
        # if there's no email in the db, cannot login
        user = User.objects.filter(email=postData['email'])
        if not user:
            errors['email_not_found'] = "Are you sure you're registered with this email?"
            return errors
        # if there is email and data is returning the information, check if password matches with the user's input information
        if not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
            errors['password'] = "Hmm.. invalid credential!"
        return errors

    def book_info_validator(self, postData):
        errors = {}
        # validating book description when user wants to add their favorite book
        # if title is not entered, cannot add
        if len(postData['title']) < 0:
            errors['title'] = "Title is required"
        # if description is less than 5, cannot add
        if len(postData['description']) < 5:
            errors['description'] = "Description must be at least 5 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    # (related_name) uploaded_books = list of books uploaded by users
    # ex) user.uploaded_books -> this will return the books that was uplodaded by user

    # (related_name) favorite_books = list of books that was liked by a given user
    # ex) user.favorite_books -> this will return the user's list of favorite books

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    # user can upload many books (one to many relationship)
    uploaded_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,  related_name="uploaded_books")
    # user can like many books and books can be liked by many users (many to many relationship)
    liked_by = models.ManyToManyField(User, related_name="favorite_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    