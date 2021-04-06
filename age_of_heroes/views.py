from django.shortcuts import render,redirect
from .models import *

# Create your views here.
query=''

def edit_patient_diagnosis(request):
    if request.method=='GET':
        query=request.GET('query')
        p=MedicalReport.objects.filter(patient__icontains=query)
        render(request,'edit-diagnosis.html',context={'patient_details' : p})
        
    return(render(request,'age_of_heroes/View-patient-diagnosis.html'))



    
