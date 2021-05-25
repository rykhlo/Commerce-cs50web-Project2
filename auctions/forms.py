from django import forms
from .models import *

class ListingForm(forms.ModelForm):
  class Meta:
    model = Listing
    fields = ['title', 'description', 'starting_bid', 'image_link']

class BidForm(forms.ModelForm):
  class Meta:
    model = Bid
    fields = ["bid_amount"]

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ["comment"]