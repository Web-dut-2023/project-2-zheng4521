from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createList", views.createList, name="createList"),
    path("listPage/<str:idnum>", views.listPage, name="listPage"),
    path("soldItems", views.soldItems, name="soldItems"),
    path("watchlist", views.FunWatchlist, name="watchlist"),
    path("category", views.FunCategory, name="category"),
    path("catItems/<str:IdCat>", views.catItems, name="catItems")
]
