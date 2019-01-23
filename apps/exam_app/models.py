from __future__ import unicode_literals
import re
from django.db import models
from datetime import *
import time
import bcrypt
EMAIL_REGEX= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors= {}
        
        if (len(postData['first_name']) < 2) or (len(postData['last_name']) < 2) or (len(postData['email']) < 1):
            errors["blank"]= "Please fill in all required fields."
        # first and last names with numbers
        if not (postData['first_name'].isalpha() and postData['last_name'].isalpha()):
            errors["alpha"]= "Names must not contain numbers."
        if (len(postData['password']) < 8):
            errors["blank"]= "Please choose a password that is at least 8 characters."
        # doesnt match email pattern
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"]= "Email address is invalid."
        if postData['password'] != postData['password_confirm']:
            errors["password"]= "Passwords do not match."
        return errors

class TripManager(models.Manager):
    def trip_validator(self, postData, user_id):
        errors= {}
        if (len(postData['destination']) <1):
            errors["blank"]= "Please enter a Destination."
        if (len(postData['description']) <1):
            errors["blank"]= "Please enter a Description."
        if len(postData['start_date']) < 1:
            errors['start_length'] = "Please select a start date."
        elif postData['start_date'] < str(datetime.today().strftime('%Y-%m-%d')):
            errors['past_start'] = "Start date cannot be before today's date."
        if len(postData['end_date']) < 1:
            errors['end_length'] = "Please select an end date."
        elif postData['end_date'] < str(datetime.today().strftime('%Y-%m-%d')):
            errors['past_end'] = "End date cannot be before today's date."
        if postData['start_date'] > postData['end_date']:
            errors['date_error'] = "Start date cannot be after the end date."
        if len(errors) >0:
            return errors
        else:
            me= User.objects.get(id= user_id)
            trip= Trip.objects.create(
                destination= postData['destination'],
                description= postData['description'],
                start_date= postData['start_date'],
                end_date= postData['end_date'],
                created_by= me
                )
            trip.vacationers.add(me)
            trip.save()
            return{}

class User(models.Model):
    first_name= models.CharField(max_length= 255)
    last_name= models.CharField(max_length= 255)
    email= models.EmailField()
    password=models.CharField(max_length= 255)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects= UserManager()


def __unicode__(self):
    return "id: " + str(self.id) + ", first_name: " + self.first_name + \
    ", last_name: " + self.last_name + ", email: " + self.email + \
    ", password: " + self.password

class Trip(models.Model):
    destination= models.CharField(max_length= 255)
    description= models.CharField(max_length= 255)
    start_date= models.DateTimeField()
    end_date= models.DateTimeField()
    created_by= models.ForeignKey(User, related_name= "created_trips")
    vacationers= models.ManyToManyField(User, related_name= "planned_vacations")
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    users= models.ManyToManyField(User, related_name= "trips")
    objects= TripManager()
   


