from django.db import models
from django.contrib.auth.models import AbstractUser

from stock_choice.models import Stock
# Create your models here.


class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)
    stocks = models.ManyToManyField(Stock)

    class Meta(AbstractUser.Meta):
    	# managed = False
    	pass