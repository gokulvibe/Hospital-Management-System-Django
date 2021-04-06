from django.urls import path, include
from . import views

urlpatterns = [
    path('patient_book_appointment', views.patient_book_appointment, name='patient_book_appointment'),
    # path('doctor_book_appointment', views.doctor_book_appointment, name='doctor_book_appointment'),
    path('appointment_booked_patient', views.appointment_booked_patient, name='appointment_booked_patient'),
    path('cancel_appointment_patient', views.cancel_appointment_patient, name='cancel_appointment_patient'),
]