from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register-staff/', views.register_staff, name='register_staff'),
    path('register-patient/', views.register_patient, name='register_patient'),
    path('register-doctor/', views.register_doctor, name='register_doctor'),
    
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]
