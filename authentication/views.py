from django.shortcuts import render
import os

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm
from django.conf import settings

from app.models import *

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            base_path = settings.BASE_DIR+"/usersdata/folder_"+username
            os.system("rm "+base_path+"/downloads/*")

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
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            
            # Use absolute paths everywhere
            base_path = os.path.join(settings.BASE_DIR, "usersdata", f"folder_{username}")
            
            # Create directories using os.makedirs instead of os.system
            os.makedirs(os.path.join(base_path, "dec_key"), exist_ok=True)
            os.makedirs(os.path.join(base_path, "enc_key"), exist_ok=True)
            os.makedirs(os.path.join(base_path, "uploads"), exist_ok=True)
            os.makedirs(os.path.join(base_path, "downloads"), exist_ok=True)
            
            # Generate key pair using subprocess instead of os.system
            private_key_path = os.path.join(base_path, "dec_key", f"{username}privatekey.pem")
            public_key_path = os.path.join(base_path, "enc_key", f"{username}publickey.pem")
            
            try:
                # For Windows, specify full path to OpenSSL if necessary
                # This uses subprocess to capture errors
                import subprocess
                
                openssl_cmd = f"openssl req -x509 -nodes -days 100000 -newkey rsa:2048 -keyout \"{private_key_path}\" -out \"{public_key_path}\" -subj \"/\""
                process = subprocess.run(openssl_cmd, shell=True, check=True, capture_output=True, text=True)
                
                print(f"Key generation output: {process.stdout}")
                if process.stderr:
                    print(f"Key generation errors: {process.stderr}")
                
                # Verify files were created
                if os.path.exists(private_key_path) and os.path.exists(public_key_path):
                    print(f"Keys successfully generated at {private_key_path} and {public_key_path}")
                else:
                    print(f"Failed to generate keys. Files don't exist at expected locations.")
            
            except Exception as e:
                print(f"Error generating keys: {str(e)}")
                # Continue with registration even if key generation fails
            
            msg = 'User created.'
            success = True
            
            #return redirect("/login/")
            username1 = User.objects.get(username=username)
            full_name = request.POST["full_name"]
            contact = request.POST["contact"]
            address = request.POST["address"]
            city = request.POST["city"]
            state = request.POST["state"]
            country = request.POST["country"]
            pincode = request.POST["pincode"]
            source_of_known = request.POST["source_of_known"]

            user_profile_info = User_Profile(username=username1, full_name=full_name, contact=contact, email=email, address=address, city=city, state=state, country=country, pincode=pincode, source_of_known=source_of_known)

            user_profile_info.save()

        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg" : msg, "success" : success })