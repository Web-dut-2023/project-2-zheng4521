from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass

class Category(models.Model):
    catName = models.CharField(max_length=64, null=True)
    

class Auction(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()
    startingPrice = models.FloatField()
    image = models.URLField(null=True)
    soldTo = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null=True, related_name='soldTo')
    soldAtPrice = models.FloatField(null=True)
    sold = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, null=True )


class Bids(models.Model):
    bidder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    product = models.ForeignKey(Auction, on_delete = models.CASCADE)
    bidPrice = models.FloatField()



class Comment(models.Model):
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    commentedOn = models.ForeignKey(Auction, on_delete = models.CASCADE)
    commentThought = models.TextField()



class Watchlist(models.Model):
    watPerson = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    watProduct = models.ForeignKey(Auction, on_delete = models.CASCADE)


