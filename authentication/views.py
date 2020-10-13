# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.shortcuts import render
import os
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm
from django.conf import settings

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "accounts/login.html", {"form": form, "msg" : msg})

def register_user(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            base_path = settings.BASE_DIR+"/usersdata/folder_"+username
            os.system("mkdir "+base_path)
            os.system("mkdir "+base_path+"/dec_key")
            os.system("mkdir "+base_path+"/enc_key")
            os.system("mkdir "+base_path+"/uploads")
            os.system("mkdir "+base_path+"/downloads")
            os.system("openssl req -x509 -nodes -days 100000 -newkey rsa:2048  -keyout usersdata/folder_"+username+"/dec_key/"+username+"privatekey.pem  -out usersdata/folder_"+username+"/enc_key/"+username+"publickey.pem  -subj '/'")
            msg     = 'User created.'
            success = True
            
            #return redirect("/login/")

        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg" : msg, "success" : success })
