from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files.storage import FileSystemStorage

class User(AbstractUser):
    birthday = models.DateField(null=True, blank=True)

class ListingCategories(models.Model):
   categories = [
   ("Auto", "Auto"),
   ("Real Estate", "Real Estate"),
   ("Electronics", "Electronics"),
   ("Fashion", "Fashion"),
   ("Home and Garden", "Home and Garden"),
   ("Sports", "Sports"),
   ("Industry and Agronomy", "Industry and Agronomy"),
   ("Antiquity", "Antiquity"),
   ("Other", "Other")
   ]

 
class AuctionListing(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=512)
    image = models.ImageField(upload_to="media/listings") 
    price = models.FloatField()
    creationDate = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=32,choices=ListingCategories.categories, default=ListingCategories.categories[-1])
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} listed by {self.author.username}"


class Bids(models.Model):
    author = models.ForeignKey(User,on_delete = models.CASCADE)
    bid = models.FloatField()
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, default=None)
    creationDate = models.DateTimeField(auto_now_add=True)
    winner = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.author} bids {self.bid} on {self.listing.title}"

class Comments(models.Model):
    author = models.ForeignKey(User,on_delete = models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, default=None)
    content = models.TextField()
    creationDate = models.DateTimeField(auto_now_add=True)

class WishList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    listings = models.ManyToManyField(AuctionListing, related_name='wishlists')

    def __str__(self):
        return f"Wishlist for {self.user.username}"