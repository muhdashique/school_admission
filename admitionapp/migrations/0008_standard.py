# Generated by Django 4.2.20 on 2025-03-24 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admitionapp', '0007_student_aadhar_number_alter_student_blood_group_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Standard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('value', models.IntegerField(unique=True)),
            ],
        ),
    ]
