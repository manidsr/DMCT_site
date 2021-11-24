from django.urls import path
from StaffApp import views

urlpatterns = [
    path("",views.GetGames,name="GetGames"),
    path("<int:IDGame>/",views.GetServers,name="GetServers"),
    path("<int:IDGame>/<int:IDServer>",views.GetItems,name="GetItems"),
    path("Offers/",views.GetOffers,name="GetOffers"),
    path("Offers/<int:IDoffer>",views.GetOffer,name="GetOffer"),
    path("SubmitForm/",views.Logout,name="Logout"),
    path("logout/",views.Logout,name="Logout"),
]