from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.models import User,auth

# Create your views here.

def login(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            user=StudentRegisterForm.objects.get(email=email)
            if check_password(password,user.password):
                request.session['email']=email
                return redirect("index")
            else:
                messages.info(request,'Password does not match')
        except StudentRegisterForm.DoesNotExist:
            messages.info(request,'Invalid email')
        
        return render(request,'login.html')
    return render(request,'login.html')

def signup(request):
    if request.method == "POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        usn=request.POST.get('usn')
        phone=request.POST.get('phone')
        branch=request.POST.get('branch')
        year=request.POST.get('year')
        gender=request.POST.get('gender')
        password=request.POST.get('password')
        password1=request.POST.get('password1') 
        pwd=make_password(password)
        try:
            StudentRegisterForm.objects.get(usn=usn)
            messages.info(request,"The USN you entered has already been taken.Please enter another USN.") 
            return render(request,'signup.html')

        except:
            try:
                StudentRegisterForm.objects.get(phone=phone)
                messages.info(request,"The Phone number you entered has already been taken.Please enter another one.")  
                return render(request,'signup.html')

            except:
                try:
                    StudentRegisterForm.objects.get(email=email)
                    messages.info(request,"The email you entered has already been taken.Please enter another one.")  
                    return render(request,'signup.html') 

                except:
                     data = StudentRegisterForm(name=name,email=email,usn=usn,phone=phone,branch=branch,year=year,gender=gender,password=pwd)
                     data.save()
                     return redirect("/")   
    return render(request,'signup.html')    

def index(request):
    try:
        request.session['email']
        if request.method == 'POST':
            suggestion=request.POST.get('suggestion_text')
            data=Suggestion(suggestion=suggestion)
            data.save()
        return render(request,'index.html')
    except:
        messages.info(request,'You are not logged in!!')
        return redirect('/')   

def events(request):
    try:
        eves=Events.objects.all()
        email=request.session['email']
        student=StudentRegisterForm.objects.get(email=email)
        context = {'eves':eves,'usn':student.usn,'name':student.name,'home_page':'active'}
        if request.method == 'POST':
            event_name=request.POST.get('event')
            event = Events.objects.get(event_name=event_name)
            try:
                Enrolment.objects.get(student=student,event=event)
                messages.info(request,"You have already Registered for this event!")
                return render(request,"events.html",context)
            except:
                all_events=list(Enrolment.objects.filter(student=student))
                for one_event in all_events:
                    if one_event.event.event_date==event.event_date:
                        messages.info(request,"You are enrolled for other event on the same day!")
                        return render(request,"events.html",context)     
        
                data = Enrolment(student=student,event=event) 
                data.save()    
                messages.success(request,"You are successfully registered")

    except:
        messages.info(request,'You are not logged in!!')
        return redirect('/')                  
    
    return render(request,"events.html",context)

def mentor(request):
    try:
        request.session['email']
        ments=Mentor.objects.all()
        context = {'ments':ments,'home_page':'active'}
        return render(request,'mentor.html',context)
    except:
        messages.info(request,'You are not logged in!!')
        return redirect('/')   

def shortlist(request):
    try:
        request.session['email']
        eves=Events.objects.all()
        mydict = {}
        for eve in eves:
            data = list(Enrolment.objects.filter(shortlist=True,event=eve))
            #print(data)
            if len(data)!=0:
                mydict[eve]=data
        #for a,b in mydict.items():
            #print(a,":",b)
        context = {'mydict':mydict,'home_page':'active'}     
        return render(request,"shortlist.html",context) 

    except:
        messages.info(request,'You are not logged in!!')
        return redirect('/')       

def logout(request):
    auth.logout(request)
    return redirect('/')  

def gallery(request):
    try:
        request.session['email']
        gals=Gallery.objects.all()
        return render(request,"gallery.html",{'gals':gals})     
    except:
        messages.info(request,'You are not logged in!!')
        return redirect('/')            


       

