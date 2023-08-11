from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:categoryName>", views.category, name="category"),
    path("listing/<str:title>", views.listing_view, name="listing"),
    path("bid/<str:title>", views.bid_view, name="bid"),
    path("close/<str:title>", views.close_view, name="close"),
    path("comment/<str:title>", views.comment_view, name="comment"),
    path("wishlist/<str:visitor>", views.wishlist_view, name="wishlist"),
    path("wishlist_add/<str:title>", views.wishlist_add, name="wishlist_add")
]
