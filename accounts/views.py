from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from .models import *
from django.contrib import messages
from django.http import HttpResponse
import string
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
# Create your views here.

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    else:
        if request.method=="POST":
            user_id=request.POST["user_id"]
            password=request.POST["password"]
            user=auth.authenticate(username=user_id,password=password)
            try:
                userObject = User.objects.get(username=user_id)
            except User.DoesNotExist:
                userObject = None
            
            if user is not None:
                auth.login(request,user)
                return redirect('/')
            
            else:
                if userObject is not None and userObject.is_active == False:
                    messages.info(request,"Your account hasn't been activated yet. Please check your Email for the activation link.")
                else:
                    messages.info(request,"Invalid Credentials")
                return redirect('login')
        else:
            return render(request,'accounts/login.html')
        
        
def logout(request):
    auth.logout(request)
    return redirect('login')


def profile(request):
    if request.user.is_authenticated:
        if StaffProfile.objects.filter(user=request.user).exists():
            return render(request, 'accounts/AS-Profile.html')
        
        elif DoctorProfile.objects.filter(user=request.user).exists():
            return render(request, 'accounts/default.html')
        
        else:
            return render(request, 'accounts/default2.html')
    
    else:
        return redirect('login')
    

#Registering staff user
def register_staff(request):
    if request.method == 'POST':
        if request.user.groups.filter(name="administrative_staff_user").exists():
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            full_name = first_name + " " + last_name
            date_of_birth = request.POST['date_of_birth']
            blood_group = request.POST['blood_group']
            age = request.POST['age']
            email = request.POST['email']
            contact_number = request.POST['contact_number']
            profile_pic = request.FILES.get('image')
            date_of_joining = request.POST['date_of_joining']
            qualification = request.POST['qualification']
            address = request.POST['address']
            gender = request.POST['gender']
            
            counter = 1
            username = "ST10STA1"
            while User.objects.filter(username=username):
                username = "ST10STA" + str(counter)
                counter += 1
                
            password = User.objects.make_random_password(6, string.ascii_lowercase)
            
            user=User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name)
            user.save()
            user.is_active = False
            user.save()
            print(username, password)
            
            print(profile_pic)
            staff_profile = StaffProfile(
                user=user,
                staff_id=username,
                staff_full_name = full_name,
                profile_picture = profile_pic,
                date_joined = date_of_joining,
                qualification = qualification,
                date_of_birth = date_of_birth,
                gender = gender,
                age = age,
                blood_group = blood_group,
                address = address,
                phone_number = contact_number)
            staff_profile.save()
            
            staff_group = Group.objects.get(name='administrative_staff_user')
            user.groups.add(staff_group)
            user.save()
            
            current_site = get_current_site(request)
            mail_subject = 'Activate your HMS account.'
            message = render_to_string('accounts/activation_email.html', {
            'user': user,
            'username': username,
            'password': password,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
            })
            email = EmailMessage(
                    mail_subject, message, to=[email]
                    )
            email.content_subtype = 'html'
            email.send()
            
            messages.info(request, "New Staff Profile has been created successfully.")
            return redirect('/')
            
        else:
            return HttpResponse("You do not have access to this submit this form")
        
    else:
        if request.user.groups.filter(name="administrative_staff_user").exists():
            return render(request, 'accounts\AS-reg.html')
        
        else:
            return HttpResponse("You do not have access to this page")


def register_patient(request):
    if request.method == 'POST':
        if request.user.groups.filter(name="administrative_staff_user").exists():
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            full_name = first_name + " " + last_name
            date_of_birth = request.POST['date_of_birth']
            blood_group = request.POST['blood_group']
            age = request.POST['age']
            diagnosis = request.POST['diagnosis']
            email = request.POST['email']
            contact_number = request.POST['contact_number']
            profile_pic = request.FILES.get('image')
            accepted_date = request.POST['accepted_date']
            address = request.POST['address']
            gender = request.POST['gender']
            
            counter = 1
            username = "ST10PAT1"
            while User.objects.filter(username=username):
                username = "ST10PAT" + str(counter)
                counter += 1
                
            password = User.objects.make_random_password(6, string.ascii_lowercase)
            
            user=User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name)
            user.save()
            user.is_active = False
            user.save()
            print(username, password)
            
            print(profile_pic)
            patient_profile = PatientProfile(
                user=user,
                patient_id=username,
                patient_full_name = full_name,
                profile_picture = profile_pic,
                accepted_date = accepted_date,
                diagnosis = diagnosis,
                date_of_birth = date_of_birth,
                gender = gender,
                age = age,
                blood_group = blood_group,
                address = address,
                phone_number = contact_number)
            patient_profile.save()
            
            current_site = get_current_site(request)
            mail_subject = 'Activate your HMS account.'
            message = render_to_string('accounts/activation_email.html', {
            'user': user,
            'username': username,
            'password': password,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
            })
            email = EmailMessage(
                    mail_subject, message, to=[email]
                    )
            email.content_subtype = 'html'
            email.send()
            
            messages.info(request, "New Patient Profile has been created successfully")
            return redirect('/')
            
        else:
            return HttpResponse("You do not have access to this submit this form")
        
    else:
        if request.user.groups.filter(name="administrative_staff_user").exists():
            return render(request, 'accounts\Patient-reg.html')
        
        else:
            return HttpResponse("You do not have access to this page")

def register_doctor(request):
    if request.method == 'POST':
        if request.user.groups.filter(name="administrative_staff_user").exists():
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            full_name = first_name + " " + last_name
            date_of_birth = request.POST['date_of_birth']
            blood_group = request.POST['blood_group']
            age = request.POST['age']
            email = request.POST['email']
            contact_number = request.POST['contact_number']
            profile_pic = request.FILES.get('image')
            date_of_joining = request.POST['date_of_joining']
            speciality = request.POST['speciality']
            address = request.POST['address']
            gender = request.POST['gender']
            
            counter = 1
            username = "ST10DOC1"
            while User.objects.filter(username=username):
                username = "ST10DOC" + str(counter)
                counter += 1
                
            password = User.objects.make_random_password(6, string.ascii_lowercase)
            
            user=User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name)
            user.save()
            user.is_active = False
            user.save()
            print(username, password)
            
            print(profile_pic)
            doctor_profile = DoctorProfile(
                user=user,
                doctor_id=username,
                doctor_full_name = full_name,
                profile_picture = profile_pic,
                date_of_joining = date_of_joining,
                speciality = speciality,
                date_of_birth = date_of_birth,
                gender = gender,
                age = age,
                blood_group = blood_group,
                address = address,
                phone_number = contact_number)
            doctor_profile.save()
            
            current_site = get_current_site(request)
            mail_subject = 'Activate your HMS account.'
            message = render_to_string('accounts/activation_email.html', {
            'user': user,
            'username': username,
            'password': password,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
            })
            email = EmailMessage(
                    mail_subject, message, to=[email]
                    )
            email.content_subtype = 'html'
            email.send()
            
            messages.info(request, "New Doctor Profile has been created successfully")
            return redirect('/')
            
        else:
            return HttpResponse("You do not have access to this submit this form")
        
    else:
        if request.user.groups.filter(name="administrative_staff_user").exists():
            return render(request, 'accounts\Doc-reg.html')
        
        else:
            return HttpResponse("You do not have access to this page")
        

def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        #login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')