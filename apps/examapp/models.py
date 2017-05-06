# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals

# from django.db import models

# # Create your models here.
from django.db import models
import bcrypt, datetime, re 
class UserManager(models.Manager):
    def register(self, data):
        error = []
        if data['dob'] == '':
		    error.append("Birthday is required.")
        elif datetime.datetime.strptime(data['dob'], '%Y-%m-%d') >= datetime.datetime.now():
			error.append("Birthday may not be in the future!!")
        if len(data['name']) <  3:
            error.append('Fields must be at least 8 characters long')
        if len(data['username']) <  3:
            error.append('Fields must be at least 8 characters long')
        if len(data['password']) <  8:
            error.append('password must be 8 characters long') 
        if len(data['confirm']) <  3:
            error.append('password must be 8 characters long') 
        if not data['name'].isalpha():
            error.append('Name must only contain letters')
        #check if username already exits
        try:
            User.objects.get(username=data['username'])
           
            error.append('username is already registered')
        except:
            pass
        #check password length
        if len(data['password'])<8:
            error.append('Password must be at least 8 characters long')
        #check if password and cofirm matches
        if data['password'] != data['confirm']:
            error.append('Password and Password Confirm must match')
        #checking if there are any errors
        if len(error) == 0:
            print('no errors')
            #bcrypt and salt password
            print 'bcrypt and salt password'
            data['password']=bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            user = User.objects.create(name=data['name'], username=data['username'], password=data['password'], birthday= data['dob'])
            return {'user': user, 'errors': 'none'}
        else:
            return {'user':'none', 'errors': error}
    
    def login(self,data):
       
        error=[]
        try:
            
            user = User.objects.get(username=data['username'])
           
           
            if bcrypt.hashpw(data['password'].encode('utf-8'), user.password.encode('utf-8')) != user.password.encode('UTF-8'):
                  
                error.append('Incorrect password.')
                
        except:
            error.append('Username has not yet been registered')

        if len(error) == 0:
            return {'user': user, 'errors': 'none'}
        else:
            return {'user': 'none', 'errors': error}

    def quoteprocess(self,data):
        error = []
        if len(data['quoteby']) < 4:
            error.append('Quoted by must be more than 3 characters')
        if len(data['quote']) < 11:
            error.append('Message must be more than 10 characters long')
        if len(error) == 0:
            return {'user': 'none', 'errors': 'none'}
        else:
            return {'user': 'none', 'errors': error}
        












            
    


class User(models.Model):
    name = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    postedby = models.CharField(max_length=45)
    quoteby = models.CharField(max_length=45)
    quote = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Favorites(models.Model):
    quote_id = models.ForeignKey(Quote)
    user_id = models.ForeignKey(User)
    objects = UserManager()
