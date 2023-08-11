from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import  HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, AuctionListing, Bids, WishList, Comments
from django.shortcuts import get_object_or_404

from .constants import ctg
from .forms import ListingForm, BidForm, CommentForm
from .utils import get_highest_bid, get_listings_by_category, add_to_wishlist, wishlist_add_util, check_ownership




def index(request):
    # Get all listings that are active and the number of listings
    listings = AuctionListing.objects.filter(active=1).all()
    totalListings = AuctionListing.objects.filter(active=1).count()
    
    # If there are no listings active, show it to the user.
    if listings is None:
        context = {
            "message": 1
        }
    else:
        context = {
            "listings": listings,
            "total": totalListings
        }

    return render(request, "auctions/index.html", context)


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
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        birthday = request.POST["birthday"]

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
            user.first_name = firstname
            user.last_name = lastname
            user.birthday = birthday
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):

    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        
        if form.is_valid():
            listing = form.save(commit=False)
            listing.author = request.user
            listing.description = request.POST['description']
            listing.save()
            
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "auctions/create.html", {
                'form': ListingForm(request.POST),
                'message': 1
            })

    return render(request, "auctions/create.html", {
        'form': ListingForm()
    })


def bid_view(request, title):
    
    if request.method == "POST":
        bidPosted = BidForm(request.POST)
        
        if bidPosted.is_valid():
            user = request.user
            listing = AuctionListing.objects.get(title=title)
            
            comments = Comments.objects.filter(listing=listing).order_by('-id')
            highestBid = get_highest_bid(listing)

            error = 0
            bidValue = bidPosted.cleaned_data['bid']

            
            # Check if the bid is lower than the starting bid
            if bidValue < listing.price:
                error = 1
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "user": user,
                    "BidForm": BidForm(),
                    "commentForm":CommentForm(),
                    "error":error,
                    "message": "The bid must be equal or higher than the listing price.",
                    "highestBid": highestBid,
                    "comments":comments
                })

            if highestBid is not None:
                if bidValue < highestBid.bid:
                    error = 1
                
            
            if error == 0:

                bid_instance = bidPosted.save(commit=False)
                bid_instance.author = user
                bid_instance.listing = listing
                bid_instance.save()

                return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "user": user,
                        "BidForm": BidForm(),
                        "commentForm":CommentForm(),
                        "error":error,
                        "message": "Success. The bid is placed.",
                        "highestBid": bid_instance,
                        "comments":comments
                })
            else:
                
                return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "user": user,
                        "BidForm": BidForm(),
                        "commentForm":CommentForm(),
                        "error":error,
                        "message": "The bid must be greater than the highest bid.",
                        "highestBid": highestBid,
                        "comments":comments
                })

    return HttpResponseRedirect(reverse("listing", args=[title]))

def listing_view(request, title):

    listing = AuctionListing.objects.get(title=title)
    user = request.user
    comments = Comments.objects.filter(listing=listing).order_by('-id')

    owner = check_ownership(user,listing)
    highestBid = get_highest_bid(listing)

    if listing.active == False:
        
        if user == highestBid.author or owner :
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "user": user,
                "BidForm": BidForm(),
                "highestBid":highestBid,
                "owner": owner,
                "comments":comments
            })
        else:
            return HttpResponseRedirect(reverse("index"))
    
   
    # check if the current listing is in the wishlist of the current user
    try:
        wishlist = user.wishlist
        wishlist_listings = wishlist.listings.all()
        if listing in wishlist_listings:
            wl = 0
        else:
            wl = 1
    except :
        wl = 1
 

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "user": user,
        "BidForm": BidForm(),
        "commentForm":CommentForm(),
        "highestBid":highestBid,
        "owner": owner,
        "comments":comments,
        "wl": wl
    })

def close_view(request,title):
    
    listing = AuctionListing.objects.get(title=title) # get the listing from the database
    allBids = Bids.objects.filter(listing=listing) # get all bids on a listing
    winnerBid = allBids.order_by('-bid')[0] # orders all bids in decreasing order and selects the first bid in the list ( the highest )
    
    winnerBid.winner = True
    listing.active = False
    user = request.user
    owner = check_ownership(user, listing)

    winnerBid.save()
    listing.save()
    comments = Comments.objects.filter(listing=listing).order_by('-id')
    
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "user": user,
        "bidForm":BidForm(),
        "highestBid":winnerBid,
        "owner": owner,
        "comments":comments
    })




def comment_view(request,title):

    if request.method == "POST":
        commentPosted = CommentForm(request.POST)
        
        if commentPosted.is_valid():

            comment_instance = commentPosted.save(commit=False)
            user = request.user
            listing = AuctionListing.objects.filter(title=title)[0]
            comment_instance.author = user
            comment_instance.listing = listing

            comment_instance.save()

            owner = check_ownership(user,listing)
            highestBid = get_highest_bid(listing)

            comments = Comments.objects.filter(listing=listing).order_by('-id')
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "user": user,
                "BidForm": BidForm(),
                "commentForm":CommentForm(),
                "highestBid":highestBid,
                "owner": owner,
                "comments": comments
            })


def wishlist_add(request, title):

    if not request.user:
        return HttpResponseRedirect(reverse("index"))

    wishlist_add_util(request,title)
    # try:
    #     listing_to_add = WishList.objects.get(user=request.user)
    # except WishList.DoesNotExist:
    #     listing_to_add = WishList(user=request.user)
    #     listing_to_add.save()     
    # listing = AuctionListing.objects.get(title=title)

    # if not listing:
    #     return HttpResponseRedirect(reverse("index"))
    

    return HttpResponseRedirect(reverse("listing", args=[title]))

def wishlist_view(request,visitor):
    if visitor == str(request.user): #str() becuase request.user is not a str object but simple lazy object.
        username = request.user
        user = get_object_or_404(User, username=username)
        try:
            wishlist = user.wishlist
        except WishList.DoesNotExist:
            return render(request, "auctions/wishlist.html", {
                "message": 1
            })

        wishlist_listings = wishlist.listings.all()
        
        return render(request, "auctions/wishlist.html", {
            "wl":wishlist_listings
        })
    else:
        return HttpResponseRedirect(reverse("index"))
        

def categories(request):

    return render(request, "auctions/categories.html", {
        "ctg": ctg
    })

def category(request,categoryName):
    listings_in_category = AuctionListing.objects.filter(category=categoryName).filter(active=1)
    if listings_in_category.exists():
        return render(request, "auctions/category.html", {
            "listings": listings_in_category,
            "category": categoryName
        })

    return render(request, "auctions/category.html", {
        "message": 1
    })