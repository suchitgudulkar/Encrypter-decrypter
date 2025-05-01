from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, FileResponse
from django import template
import os
from django.conf import settings
from subprocess import PIPE
import subprocess
from OTXv2 import OTXv2
import hashlib

API_KEY = '364a0c9c4ccffaf4de039a3bfa44b6e8f2c0c294375b2e5efccd10b7dd213f6a'
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

                # Downloads encrypted file
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
            username = request.user.username
            filename = str(request.FILES['file'])
            filename = filename.replace(" ", "_")
            base_path = settings.BASE_DIR+"/usersdata/folder_"+username
            
            # Debug print statements
            print(f"Processing file: {filename}")
            print(f"Base path: {base_path}")
            
            # Ensure directories exist
            if not os.path.exists(base_path+"/uploads/"):
                os.makedirs(base_path+"/uploads/", exist_ok=True)
            if not os.path.exists(base_path+"/downloads/"):
                os.makedirs(base_path+"/downloads/", exist_ok=True)
                
            # Clear downloads
            os.system(f"rm -f {base_path}/downloads/*")
            
            # Handle file upload
            handle_uploaded_file(request, request.FILES['file'], filename)
            
            # Check if the file was uploaded successfully
            if not os.path.exists(f"{base_path}/uploads/{filename}"):
                raise Exception(f"File was not uploaded successfully to {base_path}/uploads/{filename}")
                
            # Check for malicious content
            hash = hashlib.md5(open(base_path+"/uploads/" + filename, 'rb').read()).hexdigest()
            res = isMalicious_file(hash)
            print(f"Malicious file check result: {res}")

            if res == False:
                # Check if public key exists
                pub_key_path = f"{base_path}/enc_key/{username}publickey.pem"
                if not os.path.exists(pub_key_path):
                    raise Exception(f"Public key not found at {pub_key_path}")
                
                # Use subprocess to get error output
                cmd = f"openssl smime -encrypt -aes256 -in {base_path}/uploads/{filename} -binary -outform DEM -out {base_path}/downloads/enc_{filename} {pub_key_path}"
                print(f"Running command: {cmd}")
                process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                if process.returncode != 0:
                    raise Exception(f"OpenSSL encryption failed: {process.stderr}")

                # Remove uploaded file
                os.remove(f"{base_path}/uploads/{filename}")
                
                # Check if output file exists
                output_path = f"{base_path}/downloads/enc_{filename}"
                if not os.path.exists(output_path):
                    raise Exception(f"Encrypted file was not created at {output_path}")
                
                # Downloads encrypted file
                return FileResponse(open(output_path, 'rb'), as_attachment=True, filename=f"enc_{filename}")
            else:
                html_template = loader.get_template("access-denied.html")
                return HttpResponse(html_template.render(context, request))

        html_template = loader.get_template("enc.html")
        return HttpResponse(html_template.render(context, request))
            
    except Exception as e:
        # Log the specific error
        print(f"Encryption error: {str(e)}")
        context['error'] = str(e)
        html_template = loader.get_template('error-500.html')
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


    

