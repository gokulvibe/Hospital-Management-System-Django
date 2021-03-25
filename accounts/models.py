from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doctor_id = models.CharField(max_length=10)
    doctor_full_name = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='doctor_profile_picture/')
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20)
    age = models.IntegerField()
    speciality = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    
    
class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patient_full_name = models.CharField(max_length=50, blank=True, null=True)
    patient_id = models.CharField(max_length=10)
    profile_picture = models.ImageField(upload_to='patient_profile_picture/')
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20)
    age = models.IntegerField()
    accepted_date = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    diagnosis = models.CharField(max_length=50)
    
    
class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=10)
    staff_full_name = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='staff_profile_picture/')
    date_joined = models.DateField()
    qualification = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20)
    age = models.IntegerField()
    address = models.CharField(max_length=100)
    
    