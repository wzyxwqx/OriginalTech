from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


# Be careful! In 'INSTALLED_APPS' at setting.py
# There is an APP called 'contrib.messages'!
# Later recommend that we should use class 'Information' instead
class Message(models.Model):
	title_text = models.CharField(max_length = 20)
	context_text = models.CharField(default = '', max_length = 1000)
	pub_date = models.DateTimeField('date published')
	def __str__(self):
		return self.title_text


class Share(models.Model):
	name_text = models.CharField(max_length = 20)
	intro_text = models.CharField(max_length = 1000)
	company_text = models.CharField(max_length = 200)
	hot_index = models.IntegerField()
	def __str__(self):
		return self.name_text


class Market(models.Model):
    market_name = models.CharField(max_length=20)
    market_index = models.DecimalField(max_digits=6, decimal_places=2)
    pub_time = models.DateTimeField('date published')

    def __str__(self):
        return self.market_name
