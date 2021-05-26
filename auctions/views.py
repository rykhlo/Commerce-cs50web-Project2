import auctions
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import *
from .forms import *

def index(request):
    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.all(),
        "categories" : Category.objects.all(),
    })

@login_required(login_url='/login')
def watchlist(request):
    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.filter(watchers=request.user).all(),
        "categories" : Category.objects.all(),
    })

def category(request, category_title):
    category = Category.objects.get(title=category_title) 
    return render(request, "auctions/index.html", {
        "listings" : category.Listings.all(),
        "categories" : Category.objects.all(),        
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

@login_required(login_url='/login')
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


@login_required(login_url='/login')
def createlisting(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user
            item.title = request.POST['title']
            item.description = request.POST.get('description')
            item.category = Category.objects.get(title=str(request.POST["category"]))   
            item.starting_bid = request.POST.get('starting_bid')
            #try getting image url. If not assign default image pic
            if request.POST.get('image_link'):
                item.image_link = request.POST.get('image_link')
            else:
                item.image_link = "https://www.allianceplast.com/wp-content/uploads/2017/11/no-image.png"
            item.save()
            return HttpResponseRedirect(reverse("listing", args=(item.id,)))
        else:
            return render(request, "auctions/createlisting.html", {
                "form": form,
                "categories" : Category.objects.all(),
            })
    else:
        return render(request, "auctions/createlisting.html", {
            "categories" : Category.objects.all(),
            "form" : ListingForm(),
        })
        
@login_required(login_url='/login')
def listing(request,listing_id):
    listing = Listing.objects.get(pk=listing_id)
    isWatched = False
    if request.user in listing.watchers.all():
        isWatched = True

    if request.method == "POST":
        form = BidForm(request.POST)
        #check if form is valid and the bid amount is valid
        if form.is_valid() and (form.cleaned_data.get('bid_amount') > listing.starting_bid):
            listing.starting_bid = form.cleaned_data.get('bid_amount')
            bid = form.save(commit=False)
            bid.listing = listing
            bid.bidder = request.user
            #bid.bid_amount = form.cleaned_data.get('bid_amount')
            bid.save()
            listing.save()
            return render(request, "auctions/listing.html", {
                "listing" : listing,
                "BidCount" : len(listing.Bids.all()),
                "form" : BidForm(),
                "message" : f"Congratulations! You placed your bid ${bid.bid_amount}",
                "isWatched" : isWatched,
            })
        else:
            return render(request, "auctions/listing.html", {
            "listing" : listing,
            "BidCount" : len(listing.Bids.all()),
            "form" : BidForm(request.POST),
            "message" : "Please enter a valid bid amount",
            "isWatched" : isWatched,
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing" : listing,
            "BidCount" : len(listing.Bids.all()),
            "form" : BidForm(),
            "message" : "",
            "isWatched" : isWatched,
        })


@login_required(login_url='/login')
def togglewatchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    isWatched = True
    if request.user in listing.watchers.all():
        listing.watchers.remove(request.user)
        message = "Removed from the watchlist"
        isWatched = False
    else:
        listing.watchers.add(request.user)
        message = "Added to the watchlist"
    
    return render(request, "auctions/listing.html", {
            "listing" : listing,
            "BidCount" : len(listing.Bids.all()),
            "form" : BidForm(),
            "message" : message,
            "isWatched" : isWatched,
    })


