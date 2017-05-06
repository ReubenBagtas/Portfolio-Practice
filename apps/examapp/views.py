# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals

# from django.shortcuts import render

# # Create your views here.
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Quote, Favorites
def index(request):
    
   
    if 'id' not in request.session:
        logout_msg= 'You are not logged in'
        messages.add_message(request, messages.ERROR, logout_msg)


    return render(request, 'examapp/index.html')




def quotes(request):
    if 'id' not in request.session:
		messages.add_message(request, messages.ERROR, 'You must be logged in to view that page.')
		return redirect('/')
    data = {
        'users': User.objects.filter(id=request.session['id']),
        'quotes': Quote.objects.all(),
        
        'favorites': Favorites.objects.filter(user_id=request.session['id'])
    }
    return render(request, 'examapp/quotes.html',data)

def user(request, quote_id):
    if 'id' not in request.session:
		messages.add_message(request, messages.ERROR, 'You must be logged in to view that page.')
		return redirect('/')
    data = {
        'quotes': Quote.objects.filter(postedby=quote_id),
        'name': quote_id,
        'count': Quote.objects.filter(postedby=quote_id).count()
    }
    return render(request, 'examapp/user.html', data)

##########
    
def register(request):
    data = {
        'name': request.POST['name'],
        'username': request.POST['username'],
        'password': request.POST['password'],
        'confirm': request.POST['confirm'],
        'dob': request.POST['dob']
        }
    
    post_data = User.objects.register(data)
    if post_data['errors']== 'none':
        request.session['username'] = post_data['user'].username
        request.session['id'] = post_data['user'].id
        register_success = 'Registration Successful, Please Log in'
        messages.add_message(request, messages.ERROR, register_success)
    else:
        for error in post_data['errors']:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/')

    return redirect('/')

def login(request):
    
    data = {
        'username': request.POST['username'],
        'password': request.POST['password']
    }
    post_data = User.objects.login(data)

    if post_data['errors'] == 'none':
       
        request.session['id'] = post_data['user'].id
        request.session['username'] = post_data['user'].username
    else:
        for error in post_data['errors']:
            messages.add_message(request, messages.ERROR, error)
            return redirect('/')

    return redirect('/quotes')

def logout(request):
  
    del request.session['id']
    return redirect('/')

def quotesprocess(request):
    data = {
        'quoteby': request.POST['quoteby'],
        'quote': request.POST['quote'],
        
    }
    post_data = Quote.objects.quoteprocess(data)
    if post_data['errors'] == 'none':
        Quote.objects.create(postedby=request.session['username'], quoteby=data['quoteby'], quote=data['quote'])
    else:
         for error in post_data['errors']:
            messages.add_message(request, messages.ERROR, error)
    return redirect('/quotes')

def add(request):
    Favorites.objects.create(quote_id_id=request.POST['add'], user_id_id=request.session['id'])
    return redirect('/quotes')
def delete(request):

    Favorites.objects.filter(id=request.POST['delete']).delete()
    return redirect('/quotes')

