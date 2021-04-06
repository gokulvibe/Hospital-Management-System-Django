from django.urls import path, include
from django.conf import settings
from . import views

urlpatterns = [
    path('edit-patient-diagnosis', views.edit_patient_diagnosis,name="patient diagnosis" )
]