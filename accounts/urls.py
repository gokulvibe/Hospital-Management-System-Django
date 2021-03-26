from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register-staff/', views.register_staff, name='register_staff'),
    path('register-patient/', views.register_patient, name='register_patient'),
    path('register-doctor/', views.register_doctor, name='register_doctor'),
    
    #Account Activation Mail
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    
    #For Password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset_form.html", html_email_template_name='accounts/password_reset_email.html'),name="reset_password"),
    path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),name="password_reset_done"),
    path('reset_password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),name="password_reset_complete"),
    
]
