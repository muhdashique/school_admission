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
    nationality = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    mother_tongue = models.CharField(max_length=50, blank=True)
    religion = models.CharField(max_length=50, blank=True)
    caste = models.CharField(max_length=50, blank=True)
    blood_group = models.CharField(max_length=5, blank=True)
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
