# Generated by Django 4.2.20 on 2025-04-07 06:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admitionapp', '0022_alter_student_standard_delete_standard'),
    ]

    operations = [
        migrations.CreateModel(
            name='Standard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('value', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='student',
            name='standard',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admitionapp.standard'),
        ),
    ]
