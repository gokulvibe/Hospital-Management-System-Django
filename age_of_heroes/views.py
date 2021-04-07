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
    if StaffProfile.objects.filter(user=request.user).exists():
        if request.method=='GET':
            q=request.GET.get('query')
            if User.objects.filter(username__icontains=q).exists():
                u=user.objects.get(username__icontains = q)
                if PatientProfile.objects.filter(user=u).exists():
                    p=PatientProfile.objects.get(user=u)
                elif DoctorProfile.objects.filter(user=u).exists():
                    p=DoctorProfile.objects.get(user=u)
                else:
                    p=StaffProfile.objects.get(user=u)
                return render(request, 'age_of_heroes/edit-profiles.html',context={'profile' : p ,'query' : q})
            else:
                messages.info(request, "the account you search for doesn't exist")
                return redirect("/edit-profiles")
        elif request.method=='POST':
            pass
        else:
            return render(request,"age_of_heroes/Edit.html")
    else:
        HttpResponse("you are not allowed to access the page")

