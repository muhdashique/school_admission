from django import forms
from .models import SchoolInfo, User, Student, Parent

class MobileNumberForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['mobile']
        widgets = {
            'mobile': forms.TextInput(attrs={
                'placeholder': 'Enter Mobile Number',
                'class': 'form-control'
            }),
        }

    def clean_mobile(self):
        mobile = self.cleaned_data.get("mobile")
        if not mobile.isdigit() or len(mobile) != 10:
            raise forms.ValidationError("Enter a valid 10-digit mobile number")
        return mobile

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user']  # Exclude user field since it's set in the view
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'standard': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            # Add explicit select widgets for the dropdown fields
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'nationality': forms.Select(attrs={'class': 'form-control'}),
            'mother_tongue': forms.Select(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'religion': forms.TextInput(attrs={'class': 'form-control'}),
            'caste': forms.TextInput(attrs={'class': 'form-control'}),
            'id_mark': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'aadhar_number': forms.TextInput(attrs={'class': 'form-control'}),
            'student_photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def clean_mobile(self):
        mobile = self.cleaned_data.get("mobile")
        if not mobile.isdigit() or len(mobile) != 10:
            raise forms.ValidationError("Enter a valid 10-digit mobile number")
        return mobile

class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        exclude = ['student']  # Exclude student since it will be set in the view
        widgets = {
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_job': forms.TextInput(attrs={'class': 'form-control'}),
            'father_education': forms.TextInput(attrs={'class': 'form-control'}),
            'father_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'father_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'father_place': forms.TextInput(attrs={'class': 'form-control'}),
            'father_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_job': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_education': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mother_place': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def clean_father_mobile(self):
        mobile = self.cleaned_data.get("father_mobile")
        if not mobile.isdigit() or len(mobile) != 10:
            raise forms.ValidationError("Enter a valid 10-digit mobile number")
        return mobile
    
    def clean_mother_mobile(self):
        mobile = self.cleaned_data.get("mother_mobile")
        if not mobile.isdigit() or len(mobile) != 10:
            raise forms.ValidationError("Enter a valid 10-digit mobile number")
        return mobile

class SchoolInfoForm(forms.ModelForm):
    class Meta:
        model = SchoolInfo
        fields = ['name', 'affiliation', 'managed_by', 'address', 'phone_numbers', 'logo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'affiliation': forms.TextInput(attrs={'class': 'form-control'}),
            'managed_by': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone_numbers': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
        }