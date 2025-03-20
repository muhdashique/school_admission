from django import forms
from .models import User

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
