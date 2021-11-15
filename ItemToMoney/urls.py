"""ItemToMoney URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from UserAuth import views as v 
from django.shortcuts import redirect

def GotoSupply(response):
    return redirect("/Supply")

urlpatterns = [
    path('', GotoSupply),
    path('admin/', admin.site.urls),
    path('Supply/', include("StaffApp.urls")),
    path('register/',v.Register,name="Register"),
    path('Profile/',v.UserProfileSetting,name="UserProfileSetting"),
    path('Profile/ChengePassword',v.ChengePassword,name="ChengePassword"),
    path('',include("django.contrib.auth.urls"))
]