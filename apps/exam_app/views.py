from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages

import bcrypt
from .models import User, UserManager, Trip, TripManager
from datetime import datetime
# the index function is called when root is visited
def index(request):
    # if 'user_id' not in request.session:
        
        # return redirect("/")
    print("THIS IS THE INDEX!!!!!!!!!!!")
    if request== 'POST':
        return redirect('/')
    else:
        return render(request, "exam_app/index.html")

def success(request):
    # trip= Trip.objects.create(destination= request.POST['destination'], start_date= request.POST['start_date'], end_date= request.POST['end_date'],description= request.POST['description'] )
    print('this is the success route')
    me= User.objects.get(id=request.session['user_id'])
    context={
        "user": me,
        # "trip": User.objects.get(id= request.session['user_id']).trips.all(),
        # "all_trips": Trip.objects.exclude(users= request.session['user_id'])
        'my_trips' : Trip.objects.filter(vacationers= me),
        'not_my_trips': Trip.objects.exclude(vacationers= me)
    }
    print("THIS IS SUCCESS!!!!!!!!!!!!")
    if request.session['user_id']:
        return render(request, 'exam_app/success.html', context)
    else:
        return redirect('/')

        
def register(request):
    print("REGISTER!!!!!!!")
    # to check if info is valid
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/')
    else:
        email = request.POST['email']
        # to check if the email already exists
        try:
            User.objects.get(email=email)
            messages.error(request, "A user with this email already exists")
            return redirect('/')
        except:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            password = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())
            # creating new user
            this_user = User.objects.create(first_name = first_name, last_name = last_name, email = email, password = password)
            request.session['user_id'] = this_user.id
            errors["success"] = "Successfully registered (or logged in)!"
            return redirect('/success')

def login(request):
    email = request.POST['email']
    # to see if it has been registered
    try:
        this_user = User.objects.get(email=email)
        if bcrypt.checkpw(request.POST['password'].encode(), this_user.password.encode()):
            request.session['user_id'] = this_user.id
            messages.error(request, "Successfully registered (or logged in)!")
            print (this_user)
            return redirect('/success')
        else:
            messages.error(request, "Incorrect password")
            return redirect('/')
    except:
        messages.error(request, "Email not found")
        return redirect('/')

def add(request):
    if not 'user_id' in request.session:
        return redirect('/')
    return render(request, 'exam_app/add.html')

def createTrip(request):
    print ("this is createTrip!!!!!!!!!!!!!!!!!")
    errors= Trip.objects.trip_validator(request.POST, request.session['user_id'])
    # errors= Trip.objects.trip_validator(request.POST, request.session['user_id'])
    if len(errors) > 0:
        for tag,error in errors.items():
            messages.error(request, error)
        return redirect("/add")
    return redirect("/success")

def createJoin(request, trip_id):
    print ("this is join!!!!!!!!!!!!!!!!!")
    me= User.objects.get(id= request.session['user_id'])
    trip= Trip.objects.get(id=trip_id)
    trip.vacationers.add(me)
    # trip.save()
    return redirect("/success")

def destroyJoin(request, trip_id):
    print ("this is join!!!!!!!!!!!!!!!!!")
    me= User.objects.get(id= request.session['user_id'])
    trip= Trip.objects.get(id=trip_id)
    trip.vacationers.remove(me)
    # trip.save()
    return redirect("/success")

def show(request, trip_id):
    trip= Trip.objects.get(id= trip_id)
    context={
    'trip': trip,
    'users': User.objects.filter(planned_vacations= trip).exclude(created_trips= trip)
    }
    return render(request, "exam_app/show.html", context)


def logout(request):
    request.session['user_id'] = None
    messages.error(request, "You have successfully logged out")
    return redirect('/')
    # User.objects.create(first_name=request.POST["first_name"], last_name=request.POST["last_name"], email=request.POST["email"])
    # return render(request,"login_reg_app/success.html")


