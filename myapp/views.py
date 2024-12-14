from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.contrib.auth import logout
from django.core.mail import send_mail
import random
from BatchProject import settings


# Create your views here.
def index(request):
    user=request.session.get('cuser')
    return render(request,'index.html',{'user':user})

def userlogin(request):
    msg=""
    if request.method=='POST':
        unm=request.POST['email']
        pas=request.POST['password']

        user=signmodel.objects.filter(email=unm,password=pas)
        uid=signmodel.objects.get(email=unm)
        print("UserID:",uid.id)
        if user:
            print("Login Successfully!")
            msg="Login Successfully!"
            request.session['cuser']=unm
            request.session['uid']=uid.id
            return redirect('/')
        else:
            print("Error...Login faild!")
            msg="Error...Login faild!"
    return render(request,'userlogin.html',{'msg':msg})

def userlogut(request):
    logout(request)
    return redirect('/')

def usersignup(request):
    msg=""
    
    if request.method=='POST':
        global newReq
        newReq=signform(request.POST)
        email=""
        if newReq.is_valid():
            email=newReq.cleaned_data.get('email')
            try:
                signmodel.objects.get(email=email)
                print("Username is already exists!")
                msg="Username is already exists!"
            except signmodel.DoesNotExist:
                #Email Sending Code
                global otp
                otp=random.randint(11111,99999)
                sub="Your One Time Password"
                msg=f"Hello User!\n\nThanks for registration with us!\n\nYour one time password is {otp}.\n\nThanks & Regards!\nNotesApp Tech - Rajkot\n+91 97247 99469 | sanket@tops-int.com"
                from_ID=settings.EMAIL_HOST_USER
                to_ID=[request.POST['email']]
                send_mail(subject=sub,message=msg,from_email=from_ID,recipient_list=to_ID)

                        
                #send_mail(subject="Your One Time Password",message=f"Hello User!\n\nThanks for registration with us!\n\nYour one time password is {otp}.\n\nThanks & Regards!\nNotesApp Tech - Rajkot\n+91 97247 99469 | sanket@tops-int.com",from_email=settings.EMAIL_HOST_USER,recipient_list=['kishantoliya4@gmail.com','meetladva1684@gmail.com','kevalkotadiya509@gmail.com','pratixagoswami2000@gmail.com','k.p.jogi89@gmail.com','radhikapithadia123@gmail.com'])
                return redirect('otpverify')
        
    return render(request,'usersignup.html',{'msg':msg})

def about(request):
    user=request.session.get('cuser')
    return render(request,'about.html',{'user':user})

def contact(request):
    user=request.session.get('cuser')
    if request.method=='POST':
        newCont=contactForm(request.POST)
        if newCont.is_valid():
            newCont.save()
            print("Your response has been submitted!")

            #Email Sending
            sub="Thankyou!"
            msg=f"Hello User!\n\nThanks for connecting with us!\nWe will contact you shortly!\n\nThanks & Regards\n+919724799469 | sanket.tops@gmail.com"
            from_ID=settings.EMAIL_HOST_USER
            to_ID=[request.POST['email']]
            send_mail(subject=sub,message=msg,from_email=from_ID,recipient_list=to_ID)
        else:
            print(newCont.errors)
    return render(request,'contact.html',{'user':user})

def notes(request):
    msg=""
    user=request.session.get('cuser')
    if request.method=='POST':
        newNotes=notesForm(request.POST,request.FILES)
        if newNotes.is_valid():
            newNotes.save()
            print("Your notes has been submitted")
            msg="Your notes has been submitted"
        else:
            print(newNotes.errors)
            msg="Error!Somthing went wrong...Try again!"
    return render(request,'notes.html',{'user':user,'msg':msg})

def profile(request):
    msg=""
    user=request.session.get('cuser')
    uid=request.session.get('uid')
    cuser=signmodel.objects.get(id=uid)
    if request.method=='POST':
        updateReq=updateform(request.POST,instance=cuser)
        if updateReq.is_valid():
            updateReq.save()
            
            print("Your profile has been updated!")
            msg="Your profile has been updated!"
            return redirect('/')
        else:
            print(updateReq.errors)
            msg="Error!Something went wrong...Try again!"
    return render(request,'profile.html',{'user':user,'cuser':cuser,'msg':msg})

def otpverify(request):
    msg=""
    global otp
    global newReq
    if request.method=='POST':
        if request.POST['otp']==str(otp):
            print("Verification done!")
            newReq.save()
            return redirect('userlogin')
        else:
            print("Error!Invalid OTP")
            msg="Error!Invalid OTP"
    return render(request,'otpverify.html',{'msg':msg})