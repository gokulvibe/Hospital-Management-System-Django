from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from accounts.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages

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
    

