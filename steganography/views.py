from django.shortcuts import render, redirect
from django.http import FileResponse, JsonResponse
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import os
import uuid
from .steg import encode_message, decode_message, SteganographyException

def steganography_info(request):
    """
    View for the steganography information page
    """
    return render(request, 'steganography/info.html')

@csrf_exempt
def encode(request):
    """
    View for encoding a message into an image
    """
    if request.method == 'POST':
        try:
            # Get the image and message from the form
            image = request.FILES.get('image')
            message = request.POST.get('message')
            
            # Validate inputs
            if not image:
                return JsonResponse({'status': 'error', 'message': 'No image file provided'})
            
            if not message:
                return JsonResponse({'status': 'error', 'message': 'No message provided'})
            
            # Check file type
            if not image.name.lower().endswith(('.png', '.bmp', '.tiff', '.tif')):
                return JsonResponse({
                    'status': 'error', 
                    'message': 'Only lossless formats are supported (PNG, BMP, TIFF)'
                })
            
            # Save the uploaded image temporarily
            temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
            os.makedirs(temp_dir, exist_ok=True)
            temp_path = os.path.join(temp_dir, f"{uuid.uuid4().hex}_{image.name}")
            
            with open(temp_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            
            # Create the output directory
            output_dir = os.path.join(settings.MEDIA_ROOT, 'encoded')
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate output filename - always use .png for output
            output_filename = f"encoded_{uuid.uuid4().hex}.png"
            output_path = os.path.join(output_dir, output_filename)
            
            # Encode the message
            encode_message(temp_path, message, output_path)
            
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            # Return success response with download link
            return JsonResponse({
                'status': 'success',
                'message': 'Message encoded successfully',
                'filename': output_filename
            })
            
        except SteganographyException as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'An error occurred: {str(e)}'})
    
    return render(request, 'steganography/encode.html')

@csrf_exempt
def decode(request):
    """
    View for decoding a message from an image
    """
    if request.method == 'POST':
        try:
            # Get the image from the form
            image = request.FILES.get('image')
            
            # Validate input
            if not image:
                return JsonResponse({'status': 'error', 'message': 'No image file provided'})
            
            # Save the uploaded image temporarily
            temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
            os.makedirs(temp_dir, exist_ok=True)
            temp_path = os.path.join(temp_dir, f"{uuid.uuid4().hex}_{image.name}")
            
            with open(temp_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            
            # Decode the message
            message = decode_message(temp_path)
            
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            # Return success response with the decoded message
            return JsonResponse({
                'status': 'success',
                'message': message
            })
            
        except SteganographyException as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'An error occurred: {str(e)}'})
    
    return render(request, 'steganography/decode.html')

def download_file(request, filename):
    """
    View for downloading an encoded image
    """
    try:
        # Construct the file path
        file_path = os.path.join(settings.MEDIA_ROOT, 'encoded', filename)
        
        # Check if the file exists
        if not os.path.exists(file_path):
            messages.error(request, 'File not found')
            return redirect('steganography:encode')
        
        # Return the file as an attachment
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('steganography:encode')
