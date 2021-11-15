from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField
# Create your models here.

class Game(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Server(models.Model):
    Game = models.ForeignKey(Game,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Item(models.Model):
    Server = models.ForeignKey(Server,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    offerLimit = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class OfferRequest(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="offersrequest",null=True)
    NameUser = models.CharField(max_length=100)
    ContactWay = models.CharField(max_length=200)
    idgame = models.IntegerField()
    game = models.CharField(max_length=200)
    idserver = models.IntegerField()
    server = models.CharField(max_length=200)
    iditem = models.IntegerField()
    item = models.CharField(max_length=500)
    itemQuantity = models.CharField(max_length=500)
    ingamename = models.CharField(max_length=200)
    note = models.CharField(max_length=500)
    finalPrice = models.FloatField()
    Status = models.IntegerField()
    
    def __str__(self):
        return self.NameUser