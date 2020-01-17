from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    # main page for registration and login
    if request.method == "GET":
        return render(request, "login_app/index.html")

    # grabbing what the user input on the form
    if request.method == "POST":
        # making variable to bring the validator from models.py
        errors = User.objects.basic_validator(request.POST)
        # if there is any error that does not match the validator, direct it to the main page:
        if len(errors) > 0:
            for key, value in errors.items():
                # give each message where each section does not meet the validator!
                messages.error(request, value)
            return redirect('/')
        else:
            # if there is no error, hash the password and send user info to db
            hash_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(
                # creating each section and hash the password
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password = hash_password
            )
            # storing user's information by their id
            request.session['user_id'] = user.id
            
            return redirect("/books")

def process_login(request):
    # making variable to bring the validator from models.py
    errors = User.objects.login_validator(request.POST)
    # if there is any error that does not match the validator, direct it to the main page
    if len(errors) > 0:
        for key, value in errors.items():
            # give each message where each section does not meet the validator!
            messages.error(request, value)
        return redirect("/")
    else:
        # storing user's information with their specific id
        user = User.objects.filter(email=request.POST['email'])
        request.session['user_id'] = user[0].id
        return redirect("/books")
    
def books(request):
    # if the user is not logged into the website, they cannot login
    if not "user_id" in request.session:
        return redirect("/")
    # when user is logged in, session will store user's information by their id
    user = User.objects.get(id=request.session['user_id'])
    context = {
        "user": user,
        "all_books":Book.objects.all()
    }
    return render(request, "login_app/welcome.html", context)

def create_book(request):

    if request.method == "POST":
        errors = User.objects.book_info_validator(request.POST)
        # if there is any error that does not match the validator, direct it to the main page:
        if len(errors) > 0:
            for key, value in errors.items():
                # give each message where each section does not meet the validator!
                messages.error(request, value)
            return redirect('/welcome')
        else:
            # when user is logged in, session will store user's information by their id
            user = User.objects.get(id=request.session['user_id'])
            # taking the user's input information and creating a book list
            added_book = Book.objects.create(
                # creating the favorite book
                # grabbing the title that user inputted
                title = request.POST['title'],
                # grabbing the description that user inputted
                description = request.POST['description'],
                # grabbing who uploaded (grabbed 'uploaded_by' from models.py)
                uploaded_by = user
            )
        
            # adding the user to the list of people who liked the book
            added_book.liked_by.add(user)
            # saves it to the db
            added_book.save()
            
            return redirect("/books")

def edit(request, id):
    if request.method == "GET":
        # keep the user in session and if not, don't let them in
        if not "user_id" in request.session:
            return redirect("/")
        # grab user id in the variable
        user = User.objects.get(id=request.session['user_id'])
        context = {
            # grab book by id and make variable to use in html
            "book": Book.objects.get(id=id),
            # make variable for user that's in session to use in html
            "user": user,
            # grabbing all users who liked the book
            "liked_user": Book.objects.get(id=id).liked_by
        }
        return render(request, "login_app/edit.html", context)

    if request.method == "POST":

        edit_book = Book.objects.get(id=id)
        edit_book.description = request.POST['description']
        edit_book.save()

        return redirect("/books")

def book_info(request, id):
    # keep the user in session and if not, don't let them in
    if not "user_id" in request.session:
        return redirect("/")
    # grab user id in the variable
    user = User.objects.get(id=request.session['user_id'])
    context = {
        # grab book by id and make variable to use in html
        "book": Book.objects.get(id=id),
        # make variable for user that's in session to use in html
        "user": user,
        # grabbing all users who liked the book
        "liked_user": Book.objects.get(id=id).liked_by
    }
    return render(request, "login_app/book_info.html", context)

def add_favorites(request, id):
    # keep the user in session and if not, don't let them in
    if not "user_id" in request.session:
        return redirect("/")
    # grab user id in the variable
    user = User.objects.get(id=request.session['user_id'])
    # grab the specific book that's on the page
    book = Book.objects.get(id=id)
    #user is adding the book that was uploaded by other person to favorite book list
    book.liked_by.add(user)
    book.save()

    return redirect("/books")

def un_favorites(request, id):
    # keep the user in session and if not, don't let them in
    if not "user_id" in request.session:
        return redirect("/")
    # grab user id in the variable
    user = User.objects.get(id=request.session['user_id'])
    # grab book id in the variable
    book = Book.objects.get(id=id)
    # removing the book from favorite list
    book.liked_by.remove(user)
    book.save()

    return redirect("/books")


def delete(request, id):
    delete_book = Book.objects.get(id=id)
    delete_book.delete()
    return redirect("/books")



def logout(request):
    request.session.clear()
    return redirect("/")