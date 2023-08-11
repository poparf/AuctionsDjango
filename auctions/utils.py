from .models import User, AuctionListing, Bids, WishList, Comments
from django.http import  HttpResponseRedirect
from django.urls import reverse


################################################ UTILITY FUNCTIONS DRY ##############################################

def get_highest_bid(listing):
    allBids = Bids.objects.filter(listing=listing)
    if allBids.exists():
        return allBids.order_by('-bid').first()
    return None

#allBids = Bids.objects.filter(listing=listing)
            # if allBids.count() > 2:
            #     max = 0
            #     for bid in allBids:
            #         if max < bid.bid:
            #             max = bid.bid
            #             highestBid = bid
            # elif allBids.count() == 1:
            #     highestBid = allBids[0]
            # else:
            #     highestBid = 0

def get_listings_by_category(category):
    return AuctionListing.objects.filter(category=category, active=1)


def add_to_wishlist(user, listing):
    wishlist = WishList.objects.get_or_create(user=user)[0]
    wishlist.listings.add(listing)


def wishlist_add_util(request, title):
    if not request.user:
        return HttpResponseRedirect(reverse("index"))

    listing = AuctionListing.objects.get(title=title)
    if listing:
        add_to_wishlist(request.user, listing)
    


def check_ownership(user, listing):
    return 1 if listing.author == user else 0

################################################ UTILITY FUNCTIONS DRY ##################################################

