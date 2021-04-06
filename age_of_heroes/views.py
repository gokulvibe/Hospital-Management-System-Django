from django.shortcuts import render, redirect
from accounts.models import *
from age_of_heroes.models import *
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponse
# Create your views here.

@login_required(login_url='/login')
def patient_book_appointment(request):
    patient = PatientProfile.objects.get(user=request.user)
    if Appointment.objects.filter(patient=patient, status='pending').exists():
        messages.info(request, 'You already have an appointment pending. You can change the date if you want to.')
        return redirect('/appointment_booked_patient')
    
    if request.method == 'POST':
        doctor_id = request.POST['doctor_id']
        date = request.POST['date']
        patient = PatientProfile.objects.get(user=request.user)
        
        if doctor_id == '':
            doctors = DoctorProfile.objects.all()
            for doctor in doctors:
                appointments = Appointment.objects.filter(doctor=doctor, date=date).order_by('expected_time')
                if len(appointments) < 35:
                    if len(appointments) == 0:
                        expected_time = datetime.time(10,0,0)
                    else:
                        ###### For the new appointment's expected time, the previous appointment's expected time is got and 15 minutes is added ######
                        previous_time = appointments.last().expected_time
                        expected_time = (datetime.datetime.combine(datetime.date.today(), previous_time) + datetime.timedelta(minutes=15)).time()
                        
                    date_object = datetime.datetime.now()
                    token_id = str(doctor.user.pk) + str(date_object.day) + str(date_object.strftime("%m")) + str(date_object.year) + str(len(appointments) + 1)
                    token_number = str(len(appointments) + 1)
                    
                    new_appointment = Appointment(doctor=doctor, date=date, patient=patient, token_number=token_number, token_id=token_id, expected_time=expected_time, status='pending')
                    new_appointment.save()
                    mail_subject = 'Appointment Booked in HMS'
                    message = render_to_string('age_of_heroes/appointment_registered_email.html', {
                    'user' : request.user,
                    'appointment' : new_appointment,
                    })
                    email = EmailMessage(
                            mail_subject, message, to=[request.user.email]
                            )
                    email.content_subtype = 'html'
                    email.send()
                    break
            else:
                messages.info(request, 'No doctor is free today, contact the receptionists for more details.')
                return redirect('patient_book_appointment')
            
            messages.info(request, 'Appointment Booked Successfully!')
            return redirect('/appointment_booked_patient')     
           
        else:
            doctor = DoctorProfile.objects.get(doctor_id=doctor_id)
            appointments = Appointment.objects.filter(doctor=doctor, date=date)
        
            if len(appointments)>=35:
                messages.info(request, 'The slots for your requested Doctor is full, choose another doctor or leave the field blank, so that we will assign you an available doctor.')
                return redirect('patient_book_appointment')
            else:
                if len(appointments) == 0:
                        expected_time = datetime.time(10,0,0)
                else:
                    ###### For the new appointment's expected time, the previous appointment's expected time is got and 15 minutes is added ######
                    previous_time = appointments.last().expected_time
                    expected_time = (datetime.datetime.combine(datetime.date.today(), previous_time) + datetime.timedelta(minutes=15)).time()
                    
                date_object = datetime.datetime.now()
                token_id = str(doctor.user.pk) + str(date_object.day) + str(date_object.strftime("%m")) + str(date_object.year) + str(len(appointments) + 1)
                token_number = str(len(appointments) + 1)
                
                new_appointment = Appointment(doctor=doctor, date=date, patient=patient, token_number=token_number, token_id=token_id, expected_time=expected_time, status='pending')
                new_appointment.save()
                mail_subject = 'Appointment Booked in HMS'
                message = render_to_string('age_of_heroes/appointment_registered_email.html', {
                'user' : request.user,
                'appointment' : new_appointment,
                })
                email = EmailMessage(
                        mail_subject, message, to=[request.user.email]
                        )
                email.content_subtype = 'html'
                email.send()
                
            messages.info(request, 'Appointment Booked Successfully!')
            return redirect('/appointment_booked_patient')
    else:
        return render(request, 'age_of_heroes\Patient-Appointment.html')
    
@login_required(login_url='/login')
def appointment_booked_patient(request):
    patient = PatientProfile.objects.filter(user=request.user)[0]
    
    try:
        appointment = Appointment.objects.filter(patient=patient, status='pending')[0]
    except:
        appointment = None
    return render(request, 'age_of_heroes\\appointment_booked_patient.html', context={'appointment' : appointment})

@login_required(login_url='/login')
def cancel_appointment_patient(request):
    if request.method == 'POST':
        appointment_id = request.POST['appointment_id']
        appointment = Appointment.objects.get(pk = appointment_id)
        appointment.delete()
        
        messages.info(request, 'Appointment cancelled successfully!')
        return redirect('/appointment_booked_patient')
    
    else:
        return HttpResponse("Dude, what are you tring to do?")