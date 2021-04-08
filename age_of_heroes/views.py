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
        m.blood_sugar_level=request.POST['sugar_level']
        m.blood_pressure=request.POST['blood_pressure']
        m.weight=request.POST['weight']
        m.height=request.POST['height']
        m.current_medical_condition=request.POST['current_conditions']
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
    n=0
    if StaffProfile.objects.filter(user=request.user).exists():
        if request.method=='GET':
            q=request.GET.get('search_term')
            if User.objects.filter(username__icontains=q).exists():
                u=User.objects.get(username__icontains = q)
                if PatientProfile.objects.filter(user=u).exists():
                    p=PatientProfile.objects.get(user=u)
                    n=1
                    messages.info(request,"you searched for "+p.patient_full_name)
                    return render(request,'age_of_heroes/edit-patient-profile.html',context={'patient_details' : p ,'user' : u})
                elif DoctorProfile.objects.filter(user=u).exists():
                    p=DoctorProfile.objects.get(user=u)
                    '''messages.info(request,"you searched for "+p.doctor_full_name)
                    return render(request,'age_of_heroes/edit-patient-profile.html')'''
                else:
                    p=StaffProfile.objects.get(user=u)
                return render(request, 'age_of_heroes/edit.html',context={'profile' : p , })
            else:
                messages.info(request, "the account you search for doesn't exist")
                return redirect("/search-profile")
        elif request.method=='POST':
            email = request.POST['email']
            u=User.objects.get(email=email)
            if PatientProfile.objects.filter(user=u).exists():    
                full_name = request.POST['name']
                date_of_birth = request.POST['date_of_birth'] if request.POST['date_of_birth'] != '' else None
                blood_group = request.POST['blood_group']
                age = request.POST['age'] if request.POST['age'] != '' else None
                diagnosis = request.POST['diagnosis']
                contact_number = request.POST['contact_number']
                profile_pic = request.FILES.get('image')
                accepted_date = request.POST['accepted_date'] if request.POST['accepted_date'] != '' else None
                address = request.POST['address']
                gender = request.POST['gender']
                
                p=PatientProfile.objects.get(patient_full_name__icontains=full_name)

                u.email=email
                p.patient_full_name = full_name,
                p.profile_picture = profile_pic,
                p.accepted_date = accepted_date,
                p.diagnosis = diagnosis,
                p.date_of_birth = date_of_birth,
                p.gender = gender,
                p.age = age,
                p.blood_group = blood_group,
                p.address = address,
                p.phone_number = contact_number
                '''u.save()'''
                p.save()

                messages.info(request, "the profile is updated sucessfully")
                return render(request, 'age_of_heroes/search-profile.html')
            else:
                HttpResponse("no mf")
        else:
            return render(request,"age_of_heroes/Edit.html")
    else:
        return HttpResponse("you are not allowed to access the page")
    

