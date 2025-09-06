from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .listing_form import ListingFormClass

def index(request, message=None):
    listings = Listing.objects.all().order_by("-id")
    
    return render(request, "auctions/index.html", {
        "listings": listings, 
        "message": message
    })


def create_listing(request):
    if request.method == "POST":
        form = ListingFormClass(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            image_url = form.cleaned_data["image_url"]
            initial_price = form.cleaned_data["initial_price"]
            categories = form.cleaned_data["categories"]
            user = request.user
            
            listing_object = Listing(
                title=title,
                description=description,
                image_url=image_url,
                initial_price=initial_price,
                categories=categories,
                user=user
                )
            #tries to add it to the database
            try:
                listing_object.save()
            except IntegrityError:
                return render(request, "auctions/create.html", {
                    "form": form,
                    "error": "Title Must Be Unique",
                })
            
            return HttpResponseRedirect(reverse("index"))


    
    return render(request, "auctions/create.html", {
        "form": ListingFormClass()
    })


def listing_page(request, listing_title):
    if request.method == "POST":
        comment = request.POST.get("comment").strip()

        if comment:
            comment_object = Comment(
                content = comment,
                user = request.user,
                listing = Listing.objects.get(title=listing_title),
            )
            comment_object.save()

        return HttpResponseRedirect(reverse("listing_page", args=[listing_title]))

    listing = Listing.objects.get(title=listing_title)
    comments = Comment.objects.filter(listing=listing).order_by("-date")

    return render(request, "auctions/listing_page.html", {
        "listing": listing,
        "comments": comments,
    })


def add_watchlist(request, listing_title):
    listing_object = Listing.objects.get(title=listing_title)
    request.user.watchlist.add(listing_object)

    return HttpResponseRedirect(reverse("listing_page", args=[listing_title]))


def remove_watchlist(request, listing_title):
    listing_object = Listing.objects.get(title=listing_title)
    request.user.watchlist.remove(listing_object)

    return HttpResponseRedirect(reverse("listing_page", args=[listing_title]))


def bid(request, listing_title):
    listing_object = Listing.objects.get(title=listing_title)

    if request.method == "POST":
        bid = int(request.POST.get("bid"))
        
        #error checking the bid input
        if bid <= listing_object.highest_bid:
            return render(request, "auctions/bid.html", {
                "listing": listing_object,
                "error": "Value must be higher than the current price."
            })
        
        bid_object = Bid(
            bid = bid, 
            user = request.user,
            listing = listing_object
        )
        bid_object.save()

        listing_object.highest_bid = bid
        listing_object.save()

        return HttpResponseRedirect(reverse("index_with_message",args=["Bid Saved!"]))
    
    return render(request, "auctions/bid.html", {
        "listing": listing_object
    })


def close(request, listing_title):
    listing_object = Listing.objects.get(title=listing_title)
    listing_final_price = listing_object.highest_bid

    if listing_final_price != listing_object.initial_price:
        bid_object = Bid.objects.get(bid=listing_final_price)
        winner = bid_object.user.username

        message = f"{winner} won {listing_title}!"
        listing_object.delete()
        
        return HttpResponseRedirect(reverse("index_with_message", args=[message]))
    
    message = f"No one won {listing_title}!"    
    listing_object.delete()
    return HttpResponseRedirect(reverse("index_with_message", args=[message]))


def watchlist(request):
    listings = request.user.watchlist.all().order_by("-id")

    return render(request, "auctions/index.html", {
        "listings": listings, 
    })
    

def categories(request):
    if request.method == "POST":
        category = request.POST.get("category")

        listings = Listing.objects.filter(categories=category)
        return render(request, "auctions/index.html", {
            "listings": listings
        })

    return render(request, "auctions/categories.html", {
        "categories": CATEGORIES
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
            user = MyUser.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")