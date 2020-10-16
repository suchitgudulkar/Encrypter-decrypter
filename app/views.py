from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, FileResponse
from django import template
import os
from django.conf import settings
from subprocess import run
from subprocess import Popen, PIPE
import subprocess
from OTXv2 import OTXv2
import argparse
import IndicatorTypes
import hashlib

API_KEY = 'b8604201fee2be44a75e20fc88ba089c1d4bd231c3f473a36f8fa0334b1edc56'
OTX_SERVER = 'https://otx.alienvault.com/'
otx = OTXv2(API_KEY, server=OTX_SERVER)
from .mal_file import file_, isMalicious_file


@login_required(login_url="/login/")
def index(request):
    return render(request, "documentation.html")

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template = request.path.split('/')[-1]
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'error-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'error-500.html' )
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def decrypt_file(request):
    context = {}
    try:
        if request.method == 'POST':
            handle_uploaded_file(request,request.FILES['file'], str(request.FILES['file']))
            username = request.user.username
            filename = str(request.FILES['file'])
            filename = filename.replace(" ", "_")
            base_path = settings.BASE_DIR+"/usersdata/folder_"+username
            os.system("rm "+base_path+"/downloads/*")
            
            hash = hashlib.md5(open(base_path+"/uploads/" + filename, 'rb').read()).hexdigest()
            res = isMalicious_file(hash)
            print(res)

            if res == False:
                os.system("openssl  smime -decrypt  -in "+base_path+"/uploads/"+filename+ " -binary -inform DEM -inkey "+base_path+ "/dec_key/"+username+"privatekey.pem  -out  "+base_path+"/downloads/dec_"+filename)

                os.remove(base_path+"/uploads/"+filename)
                # filepath = os.path.join(settings.BASE_DIR, "dec_keys/dec_"+filename)
                filepath = base_path+"/downloads/dec_"+filename
            
                return FileResponse(open(filepath, 'rb'), as_attachment=True, filename="dec_"+filename[4:])
            else:
                html_template = loader.get_template( "access-denied.html" )
                return HttpResponse(html_template.render(context, request))


        html_template = loader.get_template( "index.html" )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'error-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'error-500.html' )
        return HttpResponse(html_template.render(context, request))    
        
@login_required(login_url="/login/")
def encrypt_file(request):
    context = {}
    try:
        if request.method == 'POST':
            handle_uploaded_file(request,request.FILES['file'], str(request.FILES['file']))
            username = request.user.username
            filename = str(request.FILES['file'])
            filename = filename.replace(" ", "_")


            base_path = settings.BASE_DIR+"/usersdata/folder_"+username
            os.system("rm "+base_path+"/downloads/*")

            hash = hashlib.md5(open(base_path+"/uploads/" + filename, 'rb').read()).hexdigest()
            res = isMalicious_file(hash)
            print(res)

            if res == False:
                os.system("openssl  smime  -encrypt -aes256  -in "+base_path+"/uploads/"+filename+ " -binary -outform DEM -out "+base_path+ "/downloads/enc_"+filename+" "+base_path+"/enc_key/"+username+"publickey.pem")

                os.remove(base_path+"/uploads/"+filename)
                # filepath = os.path.join(settings.BASE_DIR, "dec_keys/dec_"+filename)
                filepath = base_path+"/downloads/enc_"+filename

                return FileResponse(open(filepath, 'rb'), as_attachment=True, filename="enc_"+filename[4:])
            else:
                html_template = loader.get_template( "access-denied.html" )
                return HttpResponse(html_template.render(context, request))

        html_template = loader.get_template( "enc.html" )
        return HttpResponse(html_template.render(context, request))
            
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'error-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'error-500.html' )
        return HttpResponse(html_template.render(context, request)) 

@login_required(login_url="/login/")
def handle_uploaded_file(request, file, filename):
    filename = filename.replace(" ", "_")
    username = request.user.username
    base_path = settings.BASE_DIR+"/usersdata/folder_"+username
    if not os.path.exists(base_path+"/uploads/"):
        os.mkdir(base_path+"/uploads/")

    with open(base_path+"/uploads/" + filename, 'wb+') as destination:
        
        # print(hash)
        
        for chunk in file.chunks():
            destination.write(chunk)


    

