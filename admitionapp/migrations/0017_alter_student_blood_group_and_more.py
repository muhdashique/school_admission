# Generated by Django 4.2.20 on 2025-03-27 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admitionapp', '0016_schoolinfo_academic_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='blood_group',
            field=models.CharField(choices=[('', '-- Select Blood Group --'), ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], max_length=7),
        ),
        migrations.AlterField(
            model_name='student',
            name='mother_tongue',
            field=models.CharField(blank=True, choices=[('', '-- Select Mother Tongue --'), ('English', 'English'), ('Hindi', 'Hindi'), ('Tamil', 'Tamil'), ('Telugu', 'Telugu'), ('Malayalam', 'Malayalam'), ('Kannada', 'Kannada'), ('Bengali', 'Bengali'), ('Marathi', 'Marathi'), ('Gujarati', 'Gujarati'), ('Punjabi', 'Punjabi'), ('Other', 'Other')], max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='nationality',
            field=models.CharField(choices=[('', '-- Select Nationality --'), ('Indian', 'Indian'), ('American', 'American'), ('British', 'British'), ('Canadian', 'Canadian'), ('Australian', 'Australian'), ('Other', 'Other')], max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='sex',
            field=models.CharField(choices=[('', '-- Select Gender --'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10),
        ),
    ]
