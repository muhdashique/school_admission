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


# Add this to your forms.py file
from django import forms
from .models import Student, Parent, SchoolInfo, Standard

class StandardForm(forms.ModelForm):
    class Meta:
        model = Standard
        fields = ['name', 'value']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'value': forms.TextInput(attrs={'class': 'form-control'})
        }

class StudentForm(forms.ModelForm):
    standard = forms.ModelChoiceField(
        queryset=Standard.objects.all(),
        empty_label="-- Select Standard --",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['user', 'status', 'is_approved'] 
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sex': forms.Select(attrs={
                'class': 'form-control',
            }, choices=[
                ('', '-- Select Gender --'),
                ('Male', 'Male'),
                ('Female', 'Female'),
                ('Other', 'Other')
            ]),
            'nationality': forms.Select(attrs={
                'class': 'form-control',
            }, choices=[('', '-- Select Nationality --')] + Student.NATIONALITY_CHOICES),
            'mother_tongue': forms.Select(attrs={
                'class': 'form-control',
            }, choices=[('', '-- Select Mother Tongue --')] + Student.MOTHER_TONGUE_CHOICES),
            'blood_group': forms.Select(attrs={
                'class': 'form-control',
            }, choices=[('', '-- Select Blood Group --')] + Student.BLOOD_GROUP_CHOICES),
            'religion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Religion'}),
            'caste': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Caste'}),
            'id_mark': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter Identification Mark'}),
            'aadhar_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter 12-digit Aadhar Number'}),
            'student_photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['mobile'].widget.attrs['readonly'] = True


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        exclude = ['student']  
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
        fields = ['name', 'affiliation', 'managed_by', 'address', 'phone_numbers', 'logo', 'academic_year']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'affiliation': forms.TextInput(attrs={'class': 'form-control'}),
            'managed_by': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone_numbers': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'academic_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '2024-2025'}),
        }



 