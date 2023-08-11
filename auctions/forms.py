from django.forms import ModelForm
from .models import AuctionListing, Bids, Comments


####################################################### FORMS #######################################################

class ListingForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
   
        self.fields['title'].widget.attrs['class'] = 'form-control mx-auto mb-3'
        self.fields['image'].widget.attrs['class'] = 'form-control-file  mx-auto mb-3'
        self.fields['price'].widget.attrs['class'] = 'form-control mx-auto mb-3'
        self.fields['description'].widget.attrs['class'] = 'form-control mx-auto mb-3'
        self.fields['category'].widget.attrs['class'] = 'form-control mx-auto mb-3'
      
    class Meta:
        model = AuctionListing
        # author and creation date should be set implicitly
        fields = ["title","description", "image", "price", "category"]

class CommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['class'] = 'form-control mb-2'
        self.fields['content'].widget.attrs['rows'] = "3"
      
    class Meta:
        model = Comments
        fields = ["content"]

class BidForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bid'].widget.attrs['class'] = 'form-control mb-2'
        self.fields['bid'].widget.attrs['max'] = '1000000000'

    class Meta:
        model = Bids
        fields = ['bid']

####################################################### FORMS #######################################################
