from django.contrib import admin
from .models import Game,Server,Item,OfferRequest
# Register your models here.

admin.site.register(Game)
admin.site.register(Server)
admin.site.register(Item)
admin.site.register(OfferRequest)