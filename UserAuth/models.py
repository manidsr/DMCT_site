from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserInfo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="userinfo",null=True)
    fullname = models.CharField(max_length=200,null=True,default='')
    phonenumber = models.CharField(max_length=100,null=True,default='')
    email = models.CharField(max_length=500,null=True,default='')
    bankId = models.CharField(max_length=24,null=True,default='')
    bankIdOwner = models.CharField(max_length=100,null=True,default='')
    IDDiscord = models.CharField(max_length=500,null=True,default='')

    def __str__(self):
        return self.fullname