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

@login_required
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


def categories(request):
    pass

@login_required
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

def listing(request,listing_id):
    listing = Listing.objects.get(pk=listing_id)

    return render(request, "auctions/listing.html", {
        "listing" : listing,
        "message" : "",
    })


@login_required
def watchlist(request):
    pass