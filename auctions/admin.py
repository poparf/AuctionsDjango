from django.contrib import admin
from auctions.models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom Fields',  # Add a section title for your custom fields
            {
                'fields': ('birthday',),  # Add your custom fields here
            },
        ),
    )



class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ("active","title","author", "price", "category","creationDate")

class BidsAdmin(admin.ModelAdmin):
    list_display = ("listing", "bid", "author", "creationDate")

class CommentsAdmin(admin.ModelAdmin):
    list_display = ("listing", "author", "creationDate")

admin.site.register(User, CustomUserAdmin)
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bids, BidsAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(WishList)