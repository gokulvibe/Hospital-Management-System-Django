from django.db import models
from django.contrib.auth.models import User
from accounts.models import *
# Create your models here.

class Appointment(models.Model):
    doctor = models.ForeignKey(DoctorProfile, related_name='doctor', on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientProfile, related_name='patient', on_delete=models.CASCADE)
    date = models.DateField()
    expected_time = models.TimeField()
    token_number = models.CharField(max_length=20)
    token_id = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    
class MedicalReport(models.Model):
    patient = models.ForeignKey(PatientProfile, related_name='medical_report_patient', on_delete=models.CASCADE)
    blood_sugar_level = models.FloatField()
    blood_pressure = models.FloatField()
    body_temperature = models.FloatField()
    weight = models.FloatField()
    xray = models.BooleanField()
    mri_scan = models.BooleanField()
    blood_sodium_level = models.FloatField()
    other_diagonosis = models.TextField()
    previous_medical_conditions = models.TextField()
    current_medical_condition = models.TextField()
    cause = models.CharField(max_length=20)
    height = models.FloatField()