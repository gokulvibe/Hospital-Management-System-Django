from django.shortcuts import render
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
                userObject = User.objects.get(username=email)
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