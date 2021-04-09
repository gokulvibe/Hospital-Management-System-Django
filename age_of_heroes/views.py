from django.shortcuts import render, redirect
from accounts.models import *
from age_of_heroes.models import *
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.models import Group
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
    
    
def cancel_appointment_staff(request):
    if request.method == 'POST':
        appointment_id = request.POST['appointment_id']
        appointment = Appointment.objects.get(pk=appointment_id)
        doctor = appointment.doctor
        appointment.delete()
        staff = StaffProfile.objects.get(user=request.user)
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
        
        return redirect('/cancel_appointment_staff')
    
    try:
        search = request.GET['search']
    except:
        search = ''

    patient_profiles = PatientProfile.objects.filter(patient_id__contains = search)
    appointments = Appointment.objects.none()
    for patient in patient_profiles:
        if len(Appointment.objects.filter(patient=patient,status='pending')) != 0:
            appointments = appointments | Appointment.objects.filter(patient=patient, status='pending')
    
    if len(appointments) == 0:
        appointments = None
            
    return render(request, 'age_of_heroes\cancel_appointment_staff.html', context={'appointments' : appointments})


# Create your views here.

@login_required(login_url='/login')
def view_patient_diagnosis(request):
    if request.user.groups.filter(name="doctor").exists():
        return render(request,'age_of_heroes/view-patient-diagnosis.html')
    else:
       return HttpResponse("you don't have access to this form" )


@login_required(login_url='/login')
def edit_diagnosis(request):
    if request.method=='GET':
        if request.user.groups.filter(name="doctor").exists():
            query=request.GET['query']
            if PatientProfile.objects.filter(patient_full_name__icontains=query).exists():
                p=PatientProfile.objects.get(patient_full_name__icontains = query)
                m=MedicalReport.objects.get(patient=p.user)
                return render(request, 'age_of_heroes/edit-diagnosis.html',context={'patient_details' : p ,'medical_report' : m})
            else:
                messages.info(request, "the account you search for doesn't exist")
                return redirect("/view-patient-diagnosis")
        else:
            HttpResponse("you don't have access to this form")
    elif request.method=='POST':
        q=request.POST['patient_name']
        new=request.POST['new_conditions']
        p=PatientProfile.objects.get(patient_full_name__icontains = q)
        m=MedicalReport.objects.get(patient=p.user)
        p.patient_full_name=request.POST['patient_name']
        m.blood_sugar_level=request.POST['sugar_level']
        print(type(m.blood_sugar_level))
        m.blood_pressure=request.POST['blood_pressure']
        m.weight=request.POST['weight']
        m.height=request.POST['height']
        m.current_medical_condition=request.POST['current_conditions']
        print(type(m.current_medical_condition))
        m.current_medical_condition=m.current_medical_condition+'       '+new
        m.save()
        messages.info(request, "the diagnosis is updated sucessfully")
        return render(request, 'age_of_heroes/edit-diagnosis.html',context={'patient_details' : p ,'medical_report' : m})
    else:
        return (HttpResponse("no query"))


@login_required(login_url='/login')
def patient_diagnosis(request):
    if PatientProfile.objects.filter(user=request.user).exists():
            patient_details = PatientProfile.objects.get(user=request.user)
            medical_report= MedicalReport.objects.get(patient=patient_details.user)
            return render(request, 'age_of_heroes/Patient-Diagnosis.html', context={'patient_details' : patient_details,'medical_report':medical_report})
    else:
        return HttpResponse("you are not a patient")


@login_required(login_url='/login')
def search_profile(request):
    if request.user.groups.filter(name="administrative_staff_user").exists():
        return render(request,'age_of_heroes/search-profile.html')
    else:
       return HttpResponse("you don't have access to this form" )



@login_required(login_url='/login')
def edit_profiles(request):
    if StaffProfile.objects.filter(user=request.user).exists():
        if request.method=='GET':
            q=request.GET.get('search_term')
            if User.objects.filter(username__icontains=q).exists():
                u=User.objects.get(username__icontains = q)
                if PatientProfile.objects.filter(user=u).exists():
                    p=PatientProfile.objects.get(user=u)
                    messages.info(request,"you searched for "+p.patient_full_name)
                    return render(request,'age_of_heroes/edit-patient-profile.html',context={'patient_details' : p ,'user' : u})
                elif DoctorProfile.objects.filter(user=u).exists():
                    p=DoctorProfile.objects.get(user=u)
                    messages.info(request,"you searched for "+p.doctor_full_name)
                    return render(request,'age_of_heroes/edit-doctor-profile.html',context={'doctor_details' : p,'user' : u})
                else:
                    p=StaffProfile.objects.get(user=u)
                    messages.info(request,"you searched for "+p.staff_full_name)
                    return render(request,'age_of_heroes/edit-staff-profile.html',context={'staff_details' : p,'user' : u})
            else:
                messages.info(request, "the account you search for doesn't exist")
                return redirect("/search-profile")
        elif request.method=='POST':
            email=request.POST.get('email')
            u=User.objects.get(email=email)
            if PatientProfile.objects.filter(user=u).exists():
                patient_profile=PatientProfile.objects.get(user=u) 
                dob=patient_profile.date_of_birth
                doa=patient_profile.accepted_date

                patient_profile.patient_full_name = request.POST['name']
                patient_profile.date_of_birth = request.POST['date_of_birth'] if request.POST['date_of_birth'] != '' else dob
                patient_profile.blood_group= request.POST['blood_group']
                patient_profile.age= request.POST['age'] 
                patient_profile.diagnosis = request.POST['diagnosis']
                patient_profile.phone_number= request.POST['contact_number']
                patient_profile.profile_picture = request.FILES.get('image')
                patient_profile.accepted_date = request.POST['accepted_date'] if request.POST['accepted_date'] != '' else doa
                patient_profile.address = request.POST['address']
                patient_profile.gender = request.POST['gender']
                
                patient_profile.save()

                messages.info(request, "the profile is updated sucessfully")
                return render(request, 'age_of_heroes/search-profile.html')
            
            elif DoctorProfile.objects.filter(user=u).exists():
                d=DoctorProfile.objects.get(user=u)
                dob=d.date_of_birth
                doj=d.date_of_joining

                d.doctor_full_name = request.POST['name']
                d.date_of_birth = request.POST['date_of_birth'] if request.POST['date_of_birth'] != '' else dob
                d.blood_group = request.POST['blood_group']
                d.age = request.POST['age'] if request.POST['age'] != '' else None
                d.phone_number = request.POST['contact_number']
                d.profile_picture = request.FILES.get('image')
                d.date_of_joining = request.POST['date_of_joining'] if request.POST['date_of_joining'] != '' else doj
                d.speciality = request.POST['speciality']
                d.address = request.POST['address']
                d.gender = request.POST['gender']
                d.save()

                messages.info(request, "the profile is updated sucessfully")
                return render(request, 'age_of_heroes/search-profile.html')
            
            elif StaffProfile.objects.filter(user=u).exists():
                s = StaffProfile.objects.get(user=u)
                dob=s.date_of_birth
                doj=s.date_joined

                name=request.POST['name']
                s.staff_full_name=name
                s.date_of_birth = request.POST['date_of_birth'] if request.POST['date_of_birth'] != '' else dob
                s.blood_group = request.POST['blood_group']
                s.age = request.POST['age'] if request.POST['age'] != '' else None
                s.phone_number = request.POST['contact_number']
                s.profile_pic = request.FILES.get('image')
                s.date_joined = request.POST['date_of_joining'] if request.POST['date_of_joining'] != '' else doj
                s.qualification = request.POST['qualification']
                s.address = request.POST['address']
                s.gender = request.POST['gender']

                s.save()

                messages.info(request, "the profile is updated sucessfully")
                return render(request, 'age_of_heroes/search-profile.html')

            else:
                HttpResponse("the user is not a patient or doctor or a staff")
    else:
        return HttpResponse("you are not allowed to access the page")
    

