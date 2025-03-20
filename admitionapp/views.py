from django.shortcuts import render
from django.http import JsonResponse
from .models import User
from .forms import MobileNumberForm
from .otp_service import send_otp, verify_otp
import logging
import json
import re

# Configure logging
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')  # Using the more robust login.html


def forms(request):
    return render(request, 'form.html')

def request_otp(request):
    """Handle OTP request"""
    if request.method == "POST":
        logger.info(f"OTP request received with data: {request.POST}")
        
        # Check if we're receiving the mobile number directly or through a form
        if 'mobile' in request.POST:
            mobile = request.POST.get('mobile')
            
            # Log request details
            logger.info(f"Received OTP request for mobile: {mobile}")
            
            # Basic validation
            if not re.match(r'^\d{10}$', mobile):
                logger.error(f"Invalid mobile number format: {mobile}")
                return JsonResponse({'status': 'failed', 'message': 'Invalid Mobile Number. Please enter a 10-digit number.'})
                
            # Send OTP (this handles generation and storage internally)
            try:
                logger.info(f"Attempting to send OTP to {mobile}")
                response = send_otp(mobile)
                logger.info(f"OTP send response: {json.dumps(response)}")
                
                return JsonResponse(response)
            except Exception as e:
                logger.error(f"Error sending OTP: {str(e)}", exc_info=True)
                return JsonResponse({'status': 'failed', 'message': f'Error sending OTP: {str(e)}'})
        else:
            # Handle form submission
            form = MobileNumberForm(request.POST)
            if form.is_valid():
                mobile = form.cleaned_data['mobile']
                response = send_otp(mobile)
                logger.info(f"OTP send response (form): {json.dumps(response)}")
                return JsonResponse(response)
            else:
                logger.error(f"Form validation errors: {form.errors}")
                return JsonResponse({'status': 'failed', 'message': 'Invalid Mobile Number', 'errors': form.errors.as_json()})
    
    # For GET requests, render the form
    return render(request, "login.html", {"form": MobileNumberForm()})

def verify_otp_view(request):
    """Verify OTP and register/login user"""
    if request.method == "POST":
        mobile = request.POST.get('mobile')
        entered_otp = request.POST.get('otp')

        # Validate input data
        if not mobile or not entered_otp:
            logger.error("Missing mobile or OTP in verification request")
            return JsonResponse({'status': 'failed', 'error': 'Missing mobile or OTP'})

        # Use the verify_otp function from otp_service.py
        if verify_otp(mobile, entered_otp):
            # OTP verified, update or create user
            try:
                user, created = User.objects.get_or_create(mobile=mobile)
                user.is_verified = True
                user.save()
                
                logger.info(f"User {'created' if created else 'updated'} after OTP verification: {mobile}")
                # Redirect to forms page instead of dashboard
                return JsonResponse({'status': 'Verified', 'redirect_url': '/forms/'})
            except Exception as e:
                logger.error(f"Error updating user after OTP verification: {str(e)}", exc_info=True)
                return JsonResponse({'status': 'failed', 'error': 'Error updating user record'})
        else:
            logger.warning(f"Invalid OTP verification attempt for mobile: {mobile}")
            return JsonResponse({'status': 'failed', 'error': 'Invalid OTP'})

    return JsonResponse({'status': 'failed', 'error': 'Invalid Request'})