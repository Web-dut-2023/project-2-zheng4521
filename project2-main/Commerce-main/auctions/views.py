from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Auction, Bids, Comment, Category, Watchlist


def index(request):
    #only Those item which is not sold yet.
    vAuction = Auction.objects.filter(sold=False)
    return render(request, "auctions/index.html",{
        "vAuction": vAuction,
        "heading": "Active listing"
    })

def soldItems(request):
    # only those item which are sold.
    vAuction = Auction.objects.filter(sold=True)
    return render(request, "auctions/index.html",{
        "vAuction": vAuction,
        "heading": "Sold Items"
    })

def catItems(request,IdCat):
    # items from a particular categery.
    vAuction = Auction.objects.filter(category= IdCat, sold=False)
    nCat = Category.objects.get(id = IdCat)
    return render(request, "auctions/index.html",{
        "vAuction": vAuction,
        "nCat": nCat
    })





def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url= 'login')
def createList(request):
    if request.method == "POST":
        
        vTitle = request.POST["title"]
        vImage = request.POST["image"]
        vStartingPrice = request.POST["startingPrice"]
        vDescription = request.POST["description"]

        vCategory = request.POST["category"]

        if not  Category.objects.filter(catName= vCategory):
            cat = Category()
            cat.catName = vCategory
            cat.save()
        
        vCatForA = Category.objects.get(catName= vCategory)

        a = Auction()
        a.owner = request.user
        a.title = vTitle
        a.image = vImage
        a.startingPrice = vStartingPrice
        a.description = vDescription
        a.category = vCatForA 
     
        a.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        AllCategory = Category.objects.all()
        return render (request, "auctions/createList.html",{
            "AllCategory": AllCategory
        })


@login_required(login_url= 'login')
def listPage(request, idnum):
    # Get the product on which you want to bid. 
    vProduct = Auction.objects.get(id= idnum)

    # Get all of the previous bids on that product.
    vBid = Bids.objects.filter(product=vProduct)

    # Get all the comment on the product.
    vCom = Comment.objects.filter(commentedOn=vProduct)


    # Get the items which are saved in the users watchlist.
    instance = Watchlist.objects.filter(watPerson= request.user, watProduct= idnum)

    # Checking for the maximum price for that product.
    max_price = vProduct.startingPrice

    for i in vBid:
        if i.bidPrice > max_price:
            max_price = i.bidPrice

    # form submitted for Bids.
    if request.method == "POST" and 'BidBtn' in request.POST:
        
        # Get the bid price from the form. 
        vBidPrice = request.POST["BidPrice"]
        # Get the user who bidded on it.
        vBidder = request.user
        
        # Insert the data into Database.
        b = Bids()
        b.bidder = vBidder
        b.bidPrice = vBidPrice
        b.product = vProduct
        b.save()

        # Get the updated data from Database.
        vBid = Bids.objects.filter(product=vProduct)
        # Get the updated max price for the product to bid on.
        for i in vBid:
            if i.bidPrice > max_price:
                max_price = i.bidPrice + 1

        return render (request, "auctions/listPage.html",{
            "x":vProduct,
            "vBid": vBid,
            "max_price": max_price,
            "vCom":vCom,
            "instance":instance
        })
    
    # "Close the Auction" button is clicked.
    elif request.method == "POST" and 'CloseAuctionBtn' in request.POST:
       # Get the winner bidder and close the Auction. 
        winner_bidder = vBid.filter(bidPrice = max_price)

        # Update the Auction Table that it's sold.
        for i in winner_bidder:
            vProduct.sold = True
            vProduct.soldTo = i.bidder
            vProduct.soldAtPrice = i.bidPrice
            vProduct.save()

        return render (request, "auctions/listPage.html",{
            "x":vProduct,
            "max_price": max_price,
            "vCom":vCom
        })



    # Form Submitted for Comment.
    elif request.method == "POST" and 'CommentBtn' in request.POST:

        vComment = request.POST["comment"]
        vCommenter = request.user

        # Insert the data into Database.
        c = Comment()
        c.commenter = vCommenter
        c.commentThought = vComment
        c.commentedOn = vProduct
        c.save()

        # Get the updated data from Database.
        vCom = Comment.objects.filter(commentedOn = vProduct)

        return render (request, "auctions/listPage.html",{
            "x":vProduct,
            "vBid": vBid,
            "max_price": max_price,
            "vCom":vCom,
            "instance":instance
        })
    
    # If "Add to Watchlist Button" is clicked.
    elif request.method == "POST" and 'watchlistBtn' in request.POST:
        vPerson = request.user
        
        w = Watchlist()
        w.watPerson = vPerson
        w.watProduct = vProduct
        w.save()
            
        return render (request, "auctions/listPage.html",{
            "x":vProduct,
            "vBid": vBid,
             "max_price": max_price,
            "vCom":vCom,
            "instance":instance,
            "message": "Successfully Added to Your Watchlist !"          
            })


    # If "Remove from Watchlist Button" is clicked.
        # if it's clicked from the watchlist page. 
    elif request.method == "POST" and 'RemoveWatchlistBtn2' in request.POST:
        vPerson = request.user
        instance= Watchlist.objects.filter(watPerson= vPerson, watProduct= idnum)
        instance.delete()
        return redirect ('watchlist')
        # if it's clicked from the list page.
    elif request.method == "POST" and 'RemoveWatchlistBtn1' in request.POST:
        vPerson = request.user
        instance= Watchlist.objects.filter(watPerson= vPerson, watProduct= idnum)
        instance.delete()
        return render (request, "auctions/listPage.html",{
            "x":vProduct,
            "vBid": vBid,
             "max_price": max_price,
            "vCom":vCom,
            "instance":instance,
            "message": "Successfully Removed from Your Watchlist !"          
            })
    
    
    else:
        return render (request, "auctions/listPage.html",{
            "x":vProduct,
            "vBid": vBid,
            "max_price": max_price,
            "vCom":vCom,
            "instance":instance
        })

@login_required(login_url= 'login')
def FunWatchlist(request):
 
    vWatchlist = Watchlist.objects.filter(watPerson=request.user)
    
    vWatProduct = set()
    for i in vWatchlist:
        vWatProduct.add(i.watProduct.pk)
    
    # How to query in objects.filter against a set of id.
    vAuction = Auction.objects.filter(id__in = vWatProduct)
    
    return render(request, "auctions/watchlist.html",{
        "vAuction": vAuction,
        "heading": "Watchlist Page"
    })  
   


@login_required(login_url= 'login')
def FunCategory(request):
    AllCategory = Category.objects.all()
    
    return render (request, "auctions/category.html",{
        "AllCategory": AllCategory
    })


