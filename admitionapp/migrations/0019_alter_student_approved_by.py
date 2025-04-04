# Generated by Django 4.2.20 on 2025-03-28 06:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admitionapp', '0018_student_approved_at_student_approved_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_students', to=settings.AUTH_USER_MODEL),
        ),
    ]
