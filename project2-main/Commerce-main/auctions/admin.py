from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Auction, Bids, Comment, Category, Watchlist

class AuctionAdmin(admin.ModelAdmin):
    list_display= ("id","owner","title","description","startingPrice", "image", "sold", "soldTo", "soldAtPrice", "category")

class BidsAdmin(admin.ModelAdmin):
    list_display= ("id","bidder","product","bidPrice")

class CommentAdmin(admin.ModelAdmin):
    list_display= ("id","commenter","commentedOn","commentThought")

class CategoryAdmin(admin.ModelAdmin):
    list_display= ("id","catName")

class WatchlistAdmin(admin.ModelAdmin):
    list_display= ("id","watPerson","watProduct")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bids, BidsAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
