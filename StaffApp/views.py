from django.contrib.auth.decorators import login_required
from django.http import response
from .models import Game,Item,Server,OfferRequest
from django.shortcuts import render,redirect
from django.contrib.auth import logout
from UserAuth.models import UserInfo

# Create your views here.
@login_required(login_url='/login/')
def GetGames(response):
    try:
        #Get games from Game object
        GameList = Game.objects.all()

        if response.method == "POST":
            #Delete game
            if response.POST.get("Delete"):
                #Get id from input and delete 
                game = Game.objects.get(id=int(response.POST.get("IName")))
                game.delete()
                #redirect for pervent resubmit on refresh
                return redirect(f"/Supply",{"GameList":GameList,"TitleContainer":"Select Your Game"})
            #Add game
            elif response.POST.get("Add"):
                #Get name for creating new game
                game = Game.objects.create(name=str(response.POST.get("IName")))
                game.save()
                #redirect for pervent resubmit on refresh
                return redirect(f"/Supply",{"GameList":GameList,"TitleContainer":"Select Your Game"})
    except:
        #if anything happened redirect to main page
        return redirect(f"/Supply")
    #render
    return render(response,"StaffApp/ListGames.html",{"GameList":GameList,"TitleContainer":"Select Your Game"})

@login_required(login_url='/login/')
def GetServers(response,IDGame):
    try:
        #Get game from Game object and servers from Game object
        ourGame = Game.objects.get(id=IDGame)
        Servers = ourGame.server_set.all()
        
        if response.method == "POST":
            #Delete Server
            if response.POST.get("Delete"):
                #Get id from input and delete 
                game = ourGame.server_set.get(id=int(response.POST.get("IName")))
                game.delete()
                #redirect for pervent resubmit on refresh
                return redirect(f"/Supply/{IDGame}",{"GameList":Servers,"TitleContainer":"Select Your Server","gameName":ourGame})
            #Add Server
            elif response.POST.get("Add"):
                #Get name for creating new server
                game = ourGame.server_set.create(name=str(response.POST.get("IName")))
                game.save()
                #redirect for pervent resubmit on refresh
                return redirect(f"/Supply/{IDGame}",{"GameList":Servers,"TitleContainer":"Select Your Server","gameName":ourGame})
    except:
        #if anything happened redirect to main page
        return redirect(f"/Supply/")
    #render
    return render(response,"StaffApp/ListServers.html",{"GameList":Servers,"TitleContainer":"Select Your Server","gameName":ourGame})

@login_required(login_url='/login/')
def GetItems(response,IDGame,IDServer):
    try:
        #Get game from Game object and server from Game object and items from Server objects
        ourGame = Game.objects.get(id=IDGame)
        Server = ourGame.server_set.get(id=IDServer)
        Items = Server.item_set.all()
        
        if response.method == "POST":
            #Add offer to Offer Request list
            if response.POST.get("submit"):
                #Check for user profile info
                #if there was not any go to profile to make one
                if UserInfo.objects.filter(user=response.user).count() == 0:
                    return redirect("/Profile/")
                #if there was one but fillds was empty go to profile
                else:
                    Info = UserInfo.objects.get(user=response.user)
                    if Info.fullname == '' or Info.phonenumber == "" or Info.email == '' or Info.bankId == '' or Info.bankIdOwner == '' or Info.IDDiscord == '':
                        return redirect("/Profile/")
                #Go in all items in list
                for ouritem in Items:
                    #get ID item we curnntly in
                    IDItem = str(ouritem.id)
                    #get value from input if it was not empty
                    if response.POST.get("input"+IDItem) != '':
                        #get offer quantity form input
                        OfferQuant = int(response.POST.get("input"+IDItem))
                        #Check if input value doesn't be more than offer quant
                        if OfferQuant > ouritem.offerLimit:
                            #if offer quant was bigger set it to offer limit
                            OfferQuant = ouritem.offerLimit
                        #calculate Price for offer request
                        Price = OfferQuant * ouritem.price
                        #Get Some Values from inputs and info object
                        Info = UserInfo.objects.get(user=response.user)
                        Name = Info.fullname
                        Discord = Info.IDDiscord
                        CName = response.POST.get("CharacterN")
                        Note = response.POST.get("Note")
                        #Add item to object with current user info
                        NewOffer = OfferRequest(user=response.user,game=ourGame.name,server=Server,item=ouritem.name,itemQuantity=OfferQuant,finalPrice=Price,NameUser=Name,ContactWay=Discord,Status=1,ingamename=CName,note=Note,
                        idgame=IDGame,idserver=IDServer,iditem=IDItem)
                        NewOffer.save()
                        response.user.offersrequest.add(NewOffer)
                        #redirect for pervent resubmit on refresh
                        return redirect(f"/Supply/Offers/{NewOffer.id}")   
            #Add item to items list         
            elif response.POST.get("Add"):
                #get item information
                name = str(response.POST.get("Name"))
                PriceItem = str(response.POST.get("Price"))
                OfferLimit = str(response.POST.get("OfferLimit"))
                #save
                item = Server.item_set.create(name=name,price=PriceItem,offerLimit=OfferLimit)
                item.save()
                #redirect for pervent resubmit on refresh
                return redirect(f"/Supply/{IDGame}/{IDServer}",{"GameList":Items,"TitleContainer":"Select Your Items","gameName":ourGame,"Server":Server})
            #Delete item from list
            elif response.POST.get("Delete"):
                #Get id form input
                item = Server.item_set.get(id=response.POST.get("DeleteId"))
                #delete
                item.delete()
                #redirect for pervent resubmit on refresh
                return redirect(f"/Supply/{IDGame}/{IDServer}",{"GameList":Items,"TitleContainer":"Select Your Items","gameName":ourGame,"Server":Server})
            #Change offer limit an item
            elif response.POST.get("changeLimit"):
                #get id and new offer limit
                item = Server.item_set.get(id=response.POST.get("changeLimitId"))
                item.offerLimit = int(response.POST.get("newItemLimit"))
                #save
                item.save()
                #redirect for pervent resubmit on refresh
                return redirect(f"/Supply/{IDGame}/{IDServer}",{"GameList":Items,"TitleContainer":"Select Your Items","gameName":ourGame,"Server":Server})
            #Chage offer price an item 
            elif response.POST.get("changePrice"):
                #Get id and new price from inputs
                item = Server.item_set.get(id=response.POST.get("changePriceId"))
                item.price = int(response.POST.get("newItemPrice"))
                #save
                item.save()
                #redirect for pervent resubmit on refresh
                return redirect(f"/Supply/{IDGame}/{IDServer}",{"GameList":Items,"TitleContainer":"Select Your Items","gameName":ourGame,"Server":Server})
    except:
        #if anything happened redirect to main page
        return redirect(f"/Supply/{IDGame}/")
    #render
    return render(response,"StaffApp/ListItems.html",{"GameList":Items,"TitleContainer":"Select Your Items","gameName":ourGame,"Server":Server})

@login_required(login_url='/login/')
def GetOffers(response):

    try:
        #Get Offer
        Offers = reversed(OfferRequest.objects.all())
        if response.method == "POST":
            #Change Status to Pendig
            if response.POST.get("Pendig"):
                offer = OfferRequest.objects.get(id=int(response.POST.get("OfferId")))
                offer.Status = 1
                offer.save()
                #redirect for pervent resubmit on refresh
                return redirect("/Supply/Offers")
            #Change Status to Complete
            elif response.POST.get("Complete"):
                offer = OfferRequest.objects.get(id=int(response.POST.get("OfferId")))
                offer.Status = 2
                offer.save()
                #redirect for pervent resubmit on refresh
                return redirect("/Supply/Offers")
            #Change Status to Canceled
            elif response.POST.get("Canceled"):
                offer = OfferRequest.objects.get(id=int(response.POST.get("OfferId")))
                offer.Status = 3
                offer.save()
                #redirect for pervent resubmit on refresh
                return redirect("/Supply/Offers")
            #Change Status to Delivered
            elif response.POST.get("Delivered"):
                offer = OfferRequest.objects.get(id=int(response.POST.get("OfferId")))
                offer.Status = 4
                #Changing offer limit after changing status
                ourGame = Game.objects.get(id=offer.idgame)
                Server = ourGame.server_set.get(id=offer.idserver)
                Item = Server.item_set.get(id=offer.iditem)
                #calculate new offer limit
                Item.offerLimit -= int(offer.itemQuantity)
                #save
                Item.save()
                offer.save()
                #redirect for pervent resubmit on refresh
                return redirect("/Supply/Offers")
    except:
        #if anything happened redirect to main page
        return redirect("/Supply/Offers")
    #render
    return render(response,"StaffApp/ListOffers.html",{"Offerslist":Offers})

@login_required(login_url='/login/')
def GetOffer(response,IDoffer):

    try:
        #Get Offer
        offer = OfferRequest.objects.get(id=IDoffer)
        Info = UserInfo.objects.get(user=offer.user)

        #show privet info if user was creator of offer or user was admin
        if offer.user == response.user or response.user.is_staff:
            if response.method == "POST":
                #Change Status to Pendig
                if response.POST.get("Pendig"):
                    offer = OfferRequest.objects.get(id=int(response.POST.get("OfferId")))
                    offer.Status = 1
                    offer.save()
                    #redirect for pervent resubmit on refresh
                    return redirect("/Supply/Offers")
                #Change Status to Complete
                elif response.POST.get("Complete"):
                    offer = OfferRequest.objects.get(id=int(response.POST.get("OfferId")))
                    offer.Status = 2
                    offer.save()
                    #redirect for pervent resubmit on refresh
                    return redirect("/Supply/Offers")
                #Change Status to Canceled
                elif response.POST.get("Canceled"):
                    offer = OfferRequest.objects.get(id=int(response.POST.get("OfferId")))
                    offer.Status = 3
                    offer.save()
                    #redirect for pervent resubmit on refresh
                    return redirect("/Supply/Offers")
                #Change Status to Delivered
                elif response.POST.get("Delivered"):
                    offer = OfferRequest.objects.get(id=int(response.POST.get("OfferId")))
                    offer.Status = 4
                    #Changing offer limit after changing status
                    ourGame = Game.objects.get(name=offer.game)
                    Server = ourGame.server_set.get(name=offer.server)
                    Item = Server.item_set.get(name=offer.item)
                    #calculate new offer limit
                    Item.offerLimit -= int(offer.itemQuantity)
                    #save
                    Item.save()
                    offer.save()
                    #redirect for pervent resubmit on refresh
                    return redirect("/Supply/Offers")
            else:
                #Go to page if respone method was not POST
                return render(response,"StaffApp/Offer.html",{"info":Info,"Offer":offer})
    except:
        #if anything happened redirect to main page
        return redirect("/Supply/Offers")
    #Go to Offers page if offer was not blong to user
    return redirect("/Supply/Offers",{"info":Info,"Offer":offer})

@login_required(login_url='/login/')
def Logout(response):
    #logout
    logout(response)