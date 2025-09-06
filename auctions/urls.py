from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("/<str:message>", views.index, name="index_with_message"),
    path("create/", views.create_listing, name="create"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories/", views.categories, name="categories"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("<str:listing_title>/", views.listing_page, name="listing_page"),
    path("<str:listing_title>/add_watchlist/", views.add_watchlist, name="add_watchlist"),
    path("<str:listing_title>/remove_watchlist/", views.remove_watchlist, name="remove_watchlist"),
    path("<str:listing_title>/bid/", views.bid, name="bid"),
    path("<str:listing_title>/close", views.close, name="close"),
]
