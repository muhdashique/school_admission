from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User, Student, Parent, SchoolInfo, Standard
from .forms import MobileNumberForm, StudentForm, ParentForm, SchoolInfoForm, StandardForm
from .otp_service import send_otp, verify_otp
from django.db.models import Q
import logging
import json
import re
logger = logging.getLogger(__name__)




# index, front pge view
def index(request):
    school = SchoolInfo.objects.first()
    return render(request, 'index.html', {'school': school})



# user login function
def mobile_login(request):
    """Simulated login view - stores the mobile number in session"""
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        user = Student.objects.filter(mobile=mobile).first()  

        if user:
            request.session['registered_number'] = mobile  
            return redirect('forms')  
        else:
            return render(request, 'login.html', {'error': 'Invalid mobile number'})

    return render(request, 'login.html')





def forms(request):
    registered_number = request.session.get('registered_number', None)
    
    # Get the search query from the request
    search_query = request.GET.get('query', '').strip()
    
    # Base queryset for students
    students = Student.objects.filter(mobile=registered_number)
    
    # If there's a search query, filter the students
    if search_query:
        students = students.filter(
            Q(name__icontains=search_query) |  # Search by name
            Q(standard__name__icontains=search_query)  # Search by standard
        )
    
    student_form = StudentForm(initial={'mobile': registered_number})
    parent_form = ParentForm()
    school = SchoolInfo.objects.first()
    
    return render(request, 'form.html', {
        'student_form': student_form,
        'parent_form': parent_form,
        'students': students,
        'registered_number': registered_number,
        'title': 'Student Admission Form',
        'school': school,
        'search_query': search_query
    })




def request_otp(request):
    """Handle OTP request"""
    if request.method == "POST":
        logger.info(f"OTP request received with data: {request.POST}")
        
     
        if 'mobile' in request.POST:
            mobile = request.POST.get('mobile')
            
            
            logger.info(f"Received OTP request for mobile: {mobile}")
            
            
            if not re.match(r'^\d{10}$', mobile):
                logger.error(f"Invalid mobile number format: {mobile}")
                return JsonResponse({'status': 'failed', 'message': 'Invalid Mobile Number. Please enter a 10-digit number.'})
                
            
            try:
                logger.info(f"Attempting to send OTP to {mobile}")
                response = send_otp(mobile)
                logger.info(f"OTP send response: {json.dumps(response)}")
                
                return JsonResponse(response)
            except Exception as e:
                logger.error(f"Error sending OTP: {str(e)}", exc_info=True)
                return JsonResponse({'status': 'failed', 'message': f'Error sending OTP: {str(e)}'})
        else:
            
            form = MobileNumberForm(request.POST)
            if form.is_valid():
                mobile = form.cleaned_data['mobile']
                response = send_otp(mobile)
                logger.info(f"OTP send response (form): {json.dumps(response)}")
                return JsonResponse(response)
            else:
                logger.error(f"Form validation errors: {form.errors}")
                return JsonResponse({'status': 'failed', 'message': 'Invalid Mobile Number', 'errors': form.errors.as_json()})
    
    
    return render(request, "login.html", {"form": MobileNumberForm()})





def verify_otp_view(request):
    """Verify OTP and register/login user"""
    if request.method == "POST":
        mobile = request.POST.get('mobile')
        entered_otp = request.POST.get('otp')

       
        if not mobile or not entered_otp:
            logger.error("Missing mobile or OTP in verification request")
            return JsonResponse({'status': 'failed', 'error': 'Missing mobile or OTP'})

       
        if verify_otp(mobile, entered_otp):
           
            try:
                user, created = User.objects.get_or_create(mobile=mobile)
                user.is_verified = True
                user.save()
                
               
                request.session['registered_number'] = mobile
                
                logger.info(f"User {'created' if created else 'updated'} after OTP verification: {mobile}")
              
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
    
    
    user, created = User.objects.get_or_create(mobile=registered_number)
    
    
    school = SchoolInfo.objects.first()
    
    if request.method == 'POST':
        student_form = StudentForm(request.POST, request.FILES)
        parent_form = ParentForm(request.POST, request.FILES)
        
        logger.info("Processing form submission")
        
        
        if not student_form.is_valid():
            for field, errors in student_form.errors.items():
                for error in errors:
                    logger.error(f"Student form error in field '{field}': {error}")
                   
                    messages.error(request, f"Error in {field}: {error}")
        
        if not parent_form.is_valid():
            for field, errors in parent_form.errors.items():
                for error in errors:
                    logger.error(f"Parent form error in field '{field}': {error}")
                    
                    messages.error(request, f"Error in {field}: {error}")
        
        if student_form.is_valid() and parent_form.is_valid():
            try:
               
                student = student_form.save(commit=False)
                student.mobile = registered_number  
                student.user = user  
                student.save()
                
                logger.info(f"Student saved: {student.name}")
                
                
                parent = parent_form.save(commit=False)
                parent.student = student
                parent.save()
                logger.info(f"Parent saved for student: {student.name}")
                
               
                messages.success(request, "Student and parent information saved successfully!")
                
               
                return redirect('forms')
            
            except Exception as e:
                logger.error(f"Error saving form: {str(e)}", exc_info=True)
                messages.error(request, f"Error saving data: {str(e)}")
        else:
            
            messages.error(request, "Please correct the errors below.")
    else:
        #
        student_form = StudentForm(initial={'mobile': registered_number})
        parent_form = ParentForm()
    

        student_form.fields['mobile'].widget.attrs['readonly'] = True
  
    students = Student.objects.filter(mobile=registered_number)
    
   
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
   
    students = Student.objects.select_related('parent').all()
    
  
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




def edit_registered_student(request, student_id):
    is_mobile = request.user_agent.is_mobile
    logger.info(f"Edit request from {'mobile' if is_mobile else 'desktop'} device")
    student = get_object_or_404(Student, id=student_id)
    registered_number = request.session.get('registered_number')
    
    if not registered_number:
        messages.error(request, "Please log in first.")
        return redirect('login')
        
    if student.mobile != registered_number:
        messages.error(request, "You can only edit your own students.")
        return redirect('forms')
    
    school = SchoolInfo.objects.first()
    
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully!")
            return redirect('forms')
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'edit_user.html', {
        'form': form,
        'school': school,
        'registered_number': registered_number  # Pass this to template
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
   
    request.session.flush()
    
    
    logout(request)
    
    
    messages.success(request, "You have been logged out.")
    
   
    response = redirect("index")
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response



@login_required
def school_header(request):
    school = SchoolInfo.objects.first()  
    return render(request, 'form.html', {'school': school})




@login_required
def add_school_info(request):
    school = SchoolInfo.objects.first() 
    if request.method == "POST":
        form = SchoolInfoForm(request.POST, request.FILES, instance=school)
        if form.is_valid():
            form.save()
            messages.success(request, "School information updated successfully!")
            return redirect('admin_panel')  
    else:
        form = SchoolInfoForm(instance=school)

    return render(request, 'add_school_info.html', {'form': form})








# Standard section
@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def add_standard(request):
    if request.method == 'POST':
        form = StandardForm(request.POST)
        if form.is_valid():
            standard = form.save(commit=False)

           
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




# search bar on admin panel

@login_required
def search_students(request):
    """View to search students based on mobile, name, or standard"""
    query = request.GET.get('query', '').strip()
    
    # Base queryset with select_related for parent to reduce database queries
    students = Student.objects.select_related('parent')
    
    if query:
        # Search across multiple fields
        students = students.filter(
            Q(mobile__icontains=query) |  # Search by mobile
            Q(name__icontains=query) |    # Search by name
            Q(standard__name__icontains=query)  # Search by standard
        )
    
    school = SchoolInfo.objects.first()
    
    return render(request, 'adminpanel.html', {
        'students': students,
        'title': 'Student Search Results',
        'school': school,
        'search_query': query
    })


@login_required
def approve_student(request, student_id):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to approve students.")
        return redirect('admin_panel')
        
    student = get_object_or_404(Student, id=student_id)
    student.is_approved = True
    student.save()
    messages.success(request, f"Student {student.name} has been approved and locked for user edits.")
    return redirect('admin_panel')




@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def toggle_approval(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.is_approved = not student.is_approved  # Toggle the approval status
    student.save()
    
    messages.success(request, f"Student {student.name} status updated to {'Approved' if student.is_approved else 'Pending'}.")
    return redirect('admin_panel')


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def set_status(request, student_id, status):
    student = get_object_or_404(Student, id=student_id)
    
    if status == 'approved':
        student.is_approved = True
        student.status = 'approved'
    elif status == 'pending':
        student.is_approved = False
        student.status = 'pending'
    elif status == 'cancel':
        student.is_approved = False
        student.status = 'cancel'
    
    student.save()
    
    messages.success(request, f"Student {student.name} status updated to {student.get_status_display()}.")
    return redirect('admin_panel')




def check_session(request):
    """Check if user session is still valid"""
    return JsonResponse({
        'authenticated': 'registered_number' in request.session
    })