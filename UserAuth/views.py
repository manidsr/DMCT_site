from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from .froms import RegisterForm
from UserAuth.models import UserInfo
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.

def Register(response):
    if response.method == "POST":
        #save register form into value 
        form = RegisterForm(response.POST)
        #if form values was right
        if form.is_valid():
            #create account
            form.save()
            #redirct to login page
            return redirect("/login")
    else:
        #if anything went wrong set form to empty
        form = RegisterForm()
    #render
    return render(response,"UserAuth/register.html",{"form":form})

@login_required(login_url='/login/')
def UserProfileSetting(response):
    #value for if save btn clicked or not
    Saved = ""
    #if there was no Userinfo for current username make one
    if UserInfo.objects.filter(user=response.user).count() == 0:
        Info = UserInfo.objects.create()
        Info.save()
        response.user.userinfo.add(Info)
    else:
        #set Info to Userinfo user
        Info = UserInfo.objects.get(user=response.user)
    
    if response.method == "POST":
        #save btn
        if response.POST.get("Save"):
            fullname,phonenumber,idDiscord,email,bankid,bankidOwner = "","","","","",""
            #if any input was filled set it to value
            if response.POST.get("fullname"):
                fullname = response.POST.get("fullname")
            if response.POST.get("phonenumber"):
                phonenumber = response.POST.get("phonenumber")
            if response.POST.get("idDiscord"):
                idDiscord = response.POST.get("idDiscord")
            if response.POST.get("email"):
                email = response.POST.get("email")
            if response.POST.get("bankid"):
                bankid = response.POST.get("bankid")
            if response.POST.get("bankIdOwner"):
                bankidOwner = response.POST.get("bankIdOwner")
            #save values in Userinfo object
            Info = UserInfo.objects.get(user=response.user)
            Info.fullname = fullname
            Info.phonenumber = phonenumber
            Info.email = email
            Info.bankId = bankid
            Info.IDDiscord = idDiscord
            Info.bankIdOwner = bankidOwner
            #saved
            Info.save()
            #butten save was clicked text
            Saved = "Saved"
            #redirect for pervent resubmit on refresh
            return redirect("/Profile",{"Info":Info,"Saved":Saved})
    #render
    return render(response,"UserAuth/ProfileSetting.html",{"Info":Info,"Saved":Saved})

@login_required(login_url='/login/')
def ChengePassword(response):
    if response.method == "POST":
        if response.POST.get("submit"):
            #get User
            usr = User.objects.get(username=response.user.username)
            #Set new password
            usr.set_password(response.POST.get("password1"))
            #save
            usr.save()
            #redirect to login
            return redirect("/login")
    #render
    return render(response,"UserAuth/ChengePassword.html",{})