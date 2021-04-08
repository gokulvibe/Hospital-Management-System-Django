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
        messages.info(request, 'You already have an appointment pending. If you want to change the appointment, cancel the older appointment first and book a new one.')
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
    if PatientProfile.objects.filter(user=request.user).exists():
        patient = PatientProfile.objects.filter(user=request.user)[0]
        
        try:
            appointment = Appointment.objects.filter(patient=patient, status='pending')[0]
        except:
            appointment = None
        return render(request, 'age_of_heroes\\appointment_booked_patient.html', context={'appointment' : appointment})
    
    else:
        return HttpResponse("You do not have access to this page!")

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
    
@login_required(login_url='/login')  
def view_appointments_doctor(request):
    if DoctorProfile.objects.filter(user=request.user).exists():
        doctor = DoctorProfile.objects.filter(user=request.user)[0]
        
        appointments = Appointment.objects.filter(doctor=doctor, status='pending', date=datetime.datetime.today())
        
        
        if len(appointments) == 0:
            appointments = None
        else:
            pass
            
        return render(request, 'age_of_heroes\\Doctor-Appiontment.html', context={'appointments' : appointments})
    
    else:
        return HttpResponse("You do not have access to view this page")

@login_required(login_url='/login')      
def appointment_done_doctor(request):
    if DoctorProfile.objects.filter(user=request.user).exists():
        if request.method == 'POST':
            appointment_id = request.POST['appointment_id']
            appointment = Appointment.objects.get(pk = appointment_id)
            appointment.status = 'done'
            appointment.save()
            
            return redirect('/view_appointments_doctor')
        
        else:
            return HttpResponse("Dude, what are you trying now?")
        
    else:
        return HttpResponse("You do not have access to perform this action!")
    
    
@login_required(login_url='/login')
def appointment_pending_doctor(request):
    if DoctorProfile.objects.filter(user=request.user).exists():
        if request.method == 'POST':
            appointment_id = request.POST['appointment_id']
            appointment = Appointment.objects.get(pk = appointment_id)
            doctor = appointment.doctor
            appointment.delete()
            mail_subject = 'Appointment Booked in HMS'
            message = render_to_string('age_of_heroes/appointment_deleted_doctor_email.html', {
            'user' : request.user,
            'doctor' : doctor,
            })
            email = EmailMessage(
                    mail_subject, message, to=[request.user.email]
                    )
            email.content_subtype = 'html'
            email.send()
            
            return redirect('/view_appointments_doctor')
        
        else:
            return HttpResponse("Dude, what are you trying now?")
        
    else:
        return HttpResponse("You do not have access to perform this action!")
    
    
@login_required(login_url='/login')
def staff_book_appointment(request):
    if request.method == 'POST':
        patient_id = request.POST['patient_id']
        patient_email = request.POST['email']
        patient_phone = request.POST['phone']
        if patient_id != '':
            patient = PatientProfile.objects.filter(patient_id=patient_id)[0]
        elif patient_email != '':
            patient = PatientProfile.objects.filter(email=patient_email)[0]
        elif patient_phone != '':
            patient = PatientProfile.objects.filter(phone_number=patient_phone)[0]
        else:
            messages.info(request, 'You have to enter either Patient ID or their Email ID or their Phone Number for booking the appointment.')
            return redirect('/staff_book_appointment')
        
        
        if Appointment.objects.filter(patient=patient, status='pending').exists():
            messages.info(request, 'You already have an appointment pending. If you want to change the appointment, cancel the older appointment first and book a new one.')
            return redirect('/staff_book_appointment')
        
        doctor_id = request.POST['doctor_id']
        date = request.POST['date']
        
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
                return redirect('staff_book_appointment')
            
            messages.info(request, 'Appointment Booked Successfully!')
            return redirect('/staff_book_appointment')     
           
        else:
            doctor = DoctorProfile.objects.get(doctor_id=doctor_id)
            appointments = Appointment.objects.filter(doctor=doctor, date=date)
        
            if len(appointments)>=35:
                messages.info(request, 'The slots for your requested Doctor is full, choose another doctor or leave the field blank, so that we will assign you an available doctor.')
                return redirect('staff_book_appointment')
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
            return redirect('/staff_book_appointment')
    else:
        return render(request, 'age_of_heroes\AS-Appointment.html')