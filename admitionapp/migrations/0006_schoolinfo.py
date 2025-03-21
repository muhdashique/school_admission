# Generated by Django 4.2.20 on 2025-03-22 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admitionapp', '0005_alter_student_mobile'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('affiliation', models.CharField(max_length=255)),
                ('managed_by', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('phone_numbers', models.TextField(help_text='Separate multiple numbers with commas')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='school_logos/')),
            ],
        ),
    ]
