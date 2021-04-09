from django.urls import path, include
from django.conf import settings
from . import views

urlpatterns = [
    path('patient_book_appointment', views.patient_book_appointment, name='patient_book_appointment'),
    # path('doctor_book_appointment', views.doctor_book_appointment, name='doctor_book_appointment'),
    path('appointment_booked_patient', views.appointment_booked_patient, name='appointment_booked_patient'),
    path('cancel_appointment_patient', views.cancel_appointment_patient, name='cancel_appointment_patient'),
    path('view_appointments_doctor', views.view_appointments_doctor, name='view_appointments_doctor'),
    path('appointment_done_doctor', views.appointment_done_doctor, name='appointment_done_doctor'),
    path('appointment_pending_doctor', views.appointment_pending_doctor, name='appointment_pending_doctor'),
    path('staff_book_appointment', views.staff_book_appointment, name='staff_book_appointment'),
    path('cancel_appointment_staff', views.cancel_appointment_staff, name='cancel_appointment_staff'),
    path('view-patient-diagnosis', views.view_patient_diagnosis,name="view-patient-diagnosis" ),
    path('edit-diagnosis',views.edit_diagnosis,name="edit-diagnosis"),
    path('patient-diagnosis',views.patient_diagnosis,name="patient-diagnosis"),
    path('edit-profiles',views.edit_profiles,name="edit-profiles"),
    path('search-profile',views.search_profile,name="search-profile"),
]