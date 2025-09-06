from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime
from django.utils import timezone



CATEGORIES = [
    ("Electronics", "Electronics"),
    ("Fashion", "Fashion"),
    ("Home & Garden", "Home & Garden"),
    ("Sports & Outdoors", "Sports & Outdoors"),
    ("Toys & Games", "Toys & Games"),
    ("Books, Movies & Music", "Books, Movies & Music"),
    ("Vehicles", "Vehicles"),
    ("Collectibles & Art", "Collectibles & Art"),
    ("Other / Miscellaneous", "Other / Miscellaneous"),
]

#the listing class
class Listing(models.Model):
    title = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True, null=True, default="No description.")
    image_url = models.ImageField(upload_to="auctions/", blank=True, null=True)
    initial_price = models.IntegerField()
    highest_bid = models.IntegerField(blank=True, null=True)
    categories = models.CharField(choices=CATEGORIES)


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listings")

    #sets the default value for highest_bid
    def save(self, *args, **kwargs):
        if not self.highest_bid:
            self.highest_bid = self.initial_price
        super().save(*args, **kwargs)


#the user class
class MyUser(AbstractUser):
    watchlist = models.ManyToManyField(Listing, related_name="watchlist_users")


#the bids class
class Bid(models.Model):
    bid = models.IntegerField()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")


#the comments class
class Comment(models.Model):
    content = models.TextField()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    date = models.DateTimeField(default=timezone.now)
