from django.db import models

class User(models.Model):
    # Change this line in models.py
    mobile = models.CharField(max_length=10)  # Remove 'unique=True'
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.mobile






from django.db import models

class Student(models.Model):
    # Add this to Student model
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students', null=True)
    standard = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    age = models.CharField(max_length=20, blank=True)  # Auto-calculated
    sex = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    address = models.TextField()
    NATIONALITY_CHOICES = [
        ('Indian', 'Indian'),
        ('American', 'American'),
        ('British', 'British'),
        ('Canadian', 'Canadian'),
        ('Australian', 'Australian'),
        ('Other', 'Other'),
    ]
    nationality = models.CharField(max_length=50, choices=NATIONALITY_CHOICES)
    mobile = models.CharField(max_length=10)
    aadhar_number = models.CharField(max_length=12, blank=True, help_text="12-digit Aadhar number")
    MOTHER_TONGUE_CHOICES = [
        ('English', 'English'),
        ('Hindi', 'Hindi'),
        ('Tamil', 'Tamil'),
        ('Telugu', 'Telugu'),
        ('Malayalam', 'Malayalam'),
        ('Kannada', 'Kannada'),
        ('Bengali', 'Bengali'),
        ('Marathi', 'Marathi'),
        ('Gujarati', 'Gujarati'),
        ('Punjabi', 'Punjabi'),
        ('Other', 'Other'),
    ]
    mother_tongue = models.CharField(max_length=50, choices=MOTHER_TONGUE_CHOICES, blank=True)
    religion = models.CharField(max_length=50, blank=True)
    caste = models.CharField(max_length=50, blank=True)
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-')
    ]

    blood_group = models.CharField(max_length=7, choices=BLOOD_GROUP_CHOICES)
    id_mark = models.TextField(blank=True)
    student_photo = models.ImageField(upload_to='student_photos/', blank=True)

    def __str__(self):
        return self.name

class Parent(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    
    father_name = models.CharField(max_length=100)
    father_job = models.CharField(max_length=100, blank=True)
    father_education = models.CharField(max_length=100, blank=True)
    father_mobile = models.CharField(max_length=10)
    father_email = models.EmailField(blank=True)
    father_place = models.CharField(max_length=100, blank=True)
    father_photo = models.ImageField(upload_to='parent_photos/', blank=True)

    mother_name = models.CharField(max_length=100)
    mother_job = models.CharField(max_length=100, blank=True)
    mother_education = models.CharField(max_length=100, blank=True)
    mother_mobile = models.CharField(max_length=10)
    mother_email = models.EmailField(blank=True)
    mother_place = models.CharField(max_length=100, blank=True)
    mother_photo = models.ImageField(upload_to='parent_photos/', blank=True)

    def __str__(self):
        return f"{self.student.name}'s Parents"








from django.db import models

class SchoolInfo(models.Model):
    name = models.CharField(max_length=255)
    affiliation = models.CharField(max_length=255)
    managed_by = models.CharField(max_length=255)
    address = models.TextField()
    phone_numbers = models.TextField(help_text="Separate multiple numbers with commas")
    logo = models.ImageField(upload_to='school_logos/', blank=True, null=True)

    def __str__(self):
        return self.name




