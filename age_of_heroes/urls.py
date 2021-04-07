from django.urls import path, include
from django.conf import settings
from . import views

urlpatterns = [
    path('view-patient-diagnosis', views.view_patient_diagnosis,name="view-patient-diagnosis" ),
    path('edit-diagnosis',views.edit_diagnosis,name="edit-diagnosis"),
    path('patient-diagnosis',views.patient_diagnosis,name="patient-diagnosis"),
    path('edit-profiles',views.edit_profiles,name="edit-profiles")
]