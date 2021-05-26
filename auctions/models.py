from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Category(models.Model):
    title = models.CharField(max_length=30)
    def __str__(self):
        return self.title

class Listing(models.Model):
    title = models.CharField(max_length=254)
    description = models.TextField(max_length=3000)
    date_listed = models.DateTimeField(default=timezone.now)
    isActive = models.BooleanField(default=True)
    image_link = models.CharField(max_length=254, blank=True)
    starting_bid = models.FloatField() #essentially used to keep track of the current bid. Dont be fooled by the name!
    seller = models.ForeignKey(User, on_delete=models.PROTECT, related_name="Listings")
    buyer = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    watchers = models.ManyToManyField(User, blank=True, related_name="Watchlist")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="Listings")
    def __str__(self):
        return self.title

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="Bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Bids")
    bid_amount = models.FloatField()
    date_bidded = models.DateTimeField(auto_now=True)
    isWinner = models.BooleanField(default=False) 
    def __str__(self):
        return f"{self.bidder}: ${self.bid_amount}"

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="Comments")
    comment = models.TextField(max_length=254)
    date_commented = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.author}: {self.date_commented}"
