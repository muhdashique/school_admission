# Generated by Django 4.2.20 on 2025-03-20 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=15, unique=True)),
                ('is_verified', models.BooleanField(default=False)),
            ],
        ),
    ]
