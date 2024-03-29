from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category


def index(request):

    if request.method == "GET":
        allListings = Listing.objects.all()
    
        return render(request, "auctions/index.html",{
            "allListings" : allListings

        })

def listing(request):
    if request.method == "POST":
        listing = Listing.objects.get(pk=Listing.objects.id)

        return render(request, "auctions/listing.html",{
            "listing": listing
        })



        
    

def create_listing(request):
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request, "auctions/create.html",{
                      "categories" : allCategories
                      })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.POST["image"]
        price = request.POST["price"]
        category = request.POST["category"]
        currentUser = request.user

        categoryData = Category.objects.get(categoryName=category)

        newListing = Listing(
            owner = currentUser,
            title = title,
            description = description,
            image = image,
            category=categoryData,
            price = float(price)
        )

        newListing.save()

        return HttpResponseRedirect(reverse("index"))
        


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
