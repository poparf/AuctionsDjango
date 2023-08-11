# Auctions with bidding system done in Django
An eccomerce/e-bay like project done in Django and Boostrap.

![Captură de ecran 2023-08-11 223541](https://github.com/poparf/AuctionsDjango/assets/127143771/eb386ce0-a578-446f-b3f7-ebf62c9f1df1)


## Features

1. Admin panel from Django has all models registered and everything can be added/edited/removed interactively.
2. You can create a **listing** through a form only if you are logged in. The form is created through the model itself.
3. Register and login system.
4. View listings by categories.
5. Add a listing to a watchlist. Every user has his own watchlist and only him can see it.
6. Add comments to listings.
7. **Close auction** feature to determine the winner of the auction.
8. When a listing is closed, it will stop appearing in the listings page and only the owner and the winner can see the listing.
9. The winner is the person with the highest bid.
10. You can bid on any listing. The highest bid will be shown on the listing page.
11. Bootstrap was used for minimal design of the app. The focus was on Django.

## Known issues
1. The images on the listing page are not properly formatted. Because of the grid system if the image on the right needs more height, the one on the left will
   have white space beneath.

This project was done as a homework for the CS50 Web course ( project 2 ).  <br> Every line of code was written by me.
<br>
## There is an issue with the distribution code offered by CS50 when it comes to styling.
<br>The styling written on styles.css in the static folder are not applied because the url is formatted wrong. To fix it put a "/" after {%%} in the layout.html
<br>
```html:
<link href="{% static 'auctions/styles.css' %}/" rel="stylesheet">
