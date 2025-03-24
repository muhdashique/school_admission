from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User, Student, Parent, SchoolInfo
from .forms import MobileNumberForm, StudentForm, ParentForm, SchoolInfoForm
from .otp_service import send_otp, verify_otp
import logging
import json
import re

# Configure logging
logger = logging.getLogger(__name__)

def index(request):
    # Get school information
    school = SchoolInfo.objects.first()
    return render(request, 'index.html', {'school': school})

def mobile_login(request):
    """Simulated login view - stores the mobile number in session"""
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        user = Student.objects.filter(mobile=mobile).first()  # Check if student exists

        if user:
            request.session['registered_number'] = mobile  # Save mobile number in session
            return redirect('forms')  # Redirect to form page
        else:
            return render(request, 'login.html', {'error': 'Invalid mobile number'})

    return render(request, 'login.html')

def forms(request):
    # Get registered number from session (user's mobile number after login)
    registered_number = request.session.get('registered_number', None)
    
    students = None
    if registered_number:
        # Filter students by registered number
        students = Student.objects.filter(mobile=registered_number)
    
    student_form = StudentForm(initial={'mobile': registered_number})
    parent_form = ParentForm()
    
    # Get school information
    school = SchoolInfo.objects.first()
    
    return render(request, 'form.html', {
        'student_form': student_form,
        'parent_form': parent_form,
        'students': students,
        'registered_number': registered_number,
        'title': 'Student Admission Form',
        'school': school
    })

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
                
                # Save mobile to session
                request.session['registered_number'] = mobile
                
                logger.info(f"User {'created' if created else 'updated'} after OTP verification: {mobile}")
                # Redirect to forms page
                return JsonResponse({'status': 'Verified', 'redirect_url': '/forms/'})
            except Exception as e:
                logger.error(f"Error updating user after OTP verification: {str(e)}", exc_info=True)
                return JsonResponse({'status': 'failed', 'error': 'Error updating user record'})
        else:
            logger.warning(f"Invalid OTP verification attempt for mobile: {mobile}")
            return JsonResponse({'status': 'failed', 'error': 'Invalid OTP'})

    return JsonResponse({'status': 'failed', 'error': 'Invalid Request'})

def admission_form(request):
    registered_number = request.session.get('registered_number', None)
    
    if not registered_number:
        messages.error(request, "Please log in first.")
        return redirect('login')
    
    # Get or create user based on registered_number
    user, created = User.objects.get_or_create(mobile=registered_number)
    
    # Get school information
    school = SchoolInfo.objects.first()
    
    if request.method == 'POST':
        student_form = StudentForm(request.POST, request.FILES)
        parent_form = ParentForm(request.POST, request.FILES)
        
        logger.info("Processing form submission")
        
        # Print detailed validation errors
        if not student_form.is_valid():
            for field, errors in student_form.errors.items():
                for error in errors:
                    logger.error(f"Student form error in field '{field}': {error}")
                    # Also add as a message for the user
                    messages.error(request, f"Error in {field}: {error}")
        
        if not parent_form.is_valid():
            for field, errors in parent_form.errors.items():
                for error in errors:
                    logger.error(f"Parent form error in field '{field}': {error}")
                    # Also add as a message for the user
                    messages.error(request, f"Error in {field}: {error}")
        
        if student_form.is_valid() and parent_form.is_valid():
            try:
                # Save student with the registered mobile number
                student = student_form.save(commit=False)
                student.mobile = registered_number  # Set from session
                student.user = user  # Link to user account
                student.save()
                
                logger.info(f"Student saved: {student.name}")
                
                # Then create parent with reference to student
                parent = parent_form.save(commit=False)
                parent.student = student
                parent.save()
                logger.info(f"Parent saved for student: {student.name}")
                
                # Add success message
                messages.success(request, "Student and parent information saved successfully!")
                
                # Redirect to the form page to show updated list
                return redirect('forms')
            
            except Exception as e:
                logger.error(f"Error saving form: {str(e)}", exc_info=True)
                messages.error(request, f"Error saving data: {str(e)}")
        else:
            # Add error message
            messages.error(request, "Please correct the errors below.")
    else:
        # Create empty forms for GET request
        student_form = StudentForm(initial={'mobile': registered_number})
        parent_form = ParentForm()
    

        student_form.fields['mobile'].widget.attrs['readonly'] = True
    # Get students associated with this number
    students = Student.objects.filter(mobile=registered_number)
    
    # Render the form template with forms and school info
    return render(request, 'form.html', {
        'student_form': student_form, 
        'parent_form': parent_form,
        'students': students,
        'registered_number': registered_number,
        'title': 'Student Admission Form',
        'school': school
    })

@login_required
def admin_panel(request):
    # Get all students with related parent data (prefetch_related for optimization)
    students = Student.objects.select_related('parent').all()
    
    # Get school information
    school = SchoolInfo.objects.first()
    
    return render(request, 'adminpanel.html', {
        'students': students,
        'title': 'Student Records',
        'school': school
    })
@login_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    parent = get_object_or_404(Parent, student=student)
    
    # Get school information
    school = SchoolInfo.objects.first()

    if request.method == 'POST':
        student_form = StudentForm(request.POST, request.FILES, instance=student)
        parent_form = ParentForm(request.POST, request.FILES, instance=parent)

        if student_form.is_valid() and parent_form.is_valid():
            student_form.save()
            parent_form.save()
            messages.success(request, "Student details updated successfully!")
            return redirect('admin_panel')

    else:
        student_form = StudentForm(instance=student)
        parent_form = ParentForm(instance=parent)

    return render(request, 'edit_student.html', {
        'student_form': student_form, 
        'parent_form': parent_form,
        'school': school
    })
@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    messages.success(request, "Student record deleted successfully!")
    return redirect('admin_panel')
@login_required
def edit_registered_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    # Get school information
    school = SchoolInfo.objects.first()
    
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('admission_form')  # Redirect after saving
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'edit_user.html', {
        'form': form,
        'school': school
    })
@login_required
def student_delete(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
        student.delete()
        messages.success(request, "Student deleted successfully!")
    except Student.DoesNotExist:
        messages.error(request, "Student not found!")
    
    return redirect('student_list')  # Change this to the correct list page name

def admin_login(request):
    """Handle admin login authentication"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user is staff/admin
            if user.is_staff or user.is_superuser:
                # Log the user in using the imported auth_login
                auth_login(request, user)
                messages.success(request, "Login successful!")
                return redirect('admin_panel')
            else:
                messages.error(request, "Access denied. Admin privileges required.")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'admin_login.html')

def admin_logout(request):
    # Clear any session data
    request.session.flush()
    
    # Log the user out
    logout(request)
    
    # Add success message
    messages.success(request, "You have been logged out.")
    
    # Return with no-cache headers
    response = redirect("index")
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response



@login_required
def school_header(request):
    school = SchoolInfo.objects.first()  # Fetch the first entry
    return render(request, 'form.html', {'school': school})
@login_required
def add_school_info(request):
    school = SchoolInfo.objects.first()  # Get the first entry if exists
    if request.method == "POST":
        form = SchoolInfoForm(request.POST, request.FILES, instance=school)
        if form.is_valid():
            form.save()
            messages.success(request, "School information updated successfully!")
            return redirect('admin_panel')  # Changed from 'admin_panel' to 'forms'
    else:
        form = SchoolInfoForm(instance=school)

    return render(request, 'add_school_info.html', {'form': form})


from .models import Standard
from .forms import StandardForm
# Standard section
@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def add_standard(request):
    if request.method == 'POST':
        form = StandardForm(request.POST)
        if form.is_valid():
            standard = form.save(commit=False)

            # If no value is provided, set a default value (e.g., 0)
            if standard.value is None:
                standard.value = 0
            
            standard.save()
            messages.success(request, "Standard added successfully!")
            return redirect('standard_list')
    else:
        form = StandardForm()

    return render(request, 'add_standard.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def standard_list(request):
    """View for listing all standards"""
    standards = Standard.objects.all()
    return render(request, 'edit_standard.html', {'standards': standards})


# In views.py
@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def edit_standard(request, standard_id):
    """View for editing standards"""
    standard = get_object_or_404(Standard, id=standard_id)
    
    if request.method == 'POST':
        form = StandardForm(request.POST, instance=standard)
        if form.is_valid():
            form.save()
            messages.success(request, "Standard updated successfully!")
            return redirect('standard_list')
    else:
        form = StandardForm(instance=standard)
    
    return render(request, 'add_standard.html', {'form': form, 'editing': True})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def delete_standard(request, standard_id):
    """View for deleting standards"""
    standard = get_object_or_404(Standard, id=standard_id)
    standard.delete()
    messages.success(request, "Standard deleted successfully!")
    return redirect('standard_list')




# middilware
from django.http import JsonResponse

def check_auth(request):
    """Simple view to check if user is authenticated via AJAX"""
    return JsonResponse({
        'authenticated': request.user.is_authenticated
    })
# middleware