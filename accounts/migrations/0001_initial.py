# Generated by Django 3.1.7 on 2021-03-25 13:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_id', models.CharField(max_length=10)),
                ('staff_full_name', models.CharField(max_length=50)),
                ('profile_picture', models.ImageField(upload_to='staff_profile_picture/')),
                ('date_joined', models.DateField()),
                ('qualification', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(max_length=20)),
                ('age', models.IntegerField()),
                ('address', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PatientProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_full_name', models.CharField(max_length=50)),
                ('patient_id', models.CharField(max_length=10)),
                ('profile_picture', models.ImageField(upload_to='patient_profile_picture/')),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(max_length=20)),
                ('age', models.IntegerField()),
                ('accepted_date', models.DateField()),
                ('phone_number', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=100)),
                ('diagnosis', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DoctorProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor_id', models.CharField(max_length=10)),
                ('doctor_full_name', models.CharField(max_length=50)),
                ('profile_picture', models.ImageField(upload_to='doctor_profile_picture/')),
                ('phone_number', models.CharField(max_length=15)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(max_length=20)),
                ('age', models.IntegerField()),
                ('speciality', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
