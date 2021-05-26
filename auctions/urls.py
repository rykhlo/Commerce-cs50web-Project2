from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("category/<str:category_title>", views.category, name="category"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("userlistings", views.userlistings, name="userlistings"),
    path("userlistings/<str:filter>", views.userlistings_filter, name="userlistings_filter"),
    path("listing/<int:listing_id>/togglewatchlist", views.togglewatchlist, name="togglewatchlist"),
    path("listing/<int:listing_id>/closelisting", views.closelisting, name="closelisting"),
]
