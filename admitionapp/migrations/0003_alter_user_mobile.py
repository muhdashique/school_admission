# Generated by Django 4.2.20 on 2025-03-21 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admitionapp', '0002_student_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.CharField(max_length=10),
        ),
    ]
