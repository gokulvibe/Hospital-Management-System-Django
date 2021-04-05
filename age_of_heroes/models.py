from django.db import models

# Create your models here.

class Appointment(models.Model):
    doctor = models.ForeignKey(User, related_name='doctor', on_delete=models.CASCADE)
    patient = models.ForeignKey(User, related_name='patient', on_delete=models.CASCADE)
    time_slot = models.DateTimeField()
    status = models.CharField()
    
class MedicalReport(models.Model):
    patient = models.ForeignKey(User, related_name='patient', on_delete=models.CASCADE)
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
    cause = models.CharField()
    height = models.FloatField()