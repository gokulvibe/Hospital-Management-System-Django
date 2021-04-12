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
    blood_sugar_level = models.FloatField(blank=True, null=True)
    blood_pressure = models.FloatField(blank=True, null=True)
    body_temperature = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    xray = models.BooleanField(default=False)
    mri_scan = models.BooleanField(default=False)
    blood_sodium_level = models.FloatField(blank=True, null=True)
    other_diagonosis = models.TextField(blank=True, null=True)
    previous_medical_conditions = models.TextField(blank=True, null=True)
    current_medical_condition = models.TextField(blank=True, null=True)
    cause = models.CharField(max_length=100)
    height = models.FloatField(blank=True, null=True)

    