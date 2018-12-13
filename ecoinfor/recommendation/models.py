from django.db import models
from django.utils import timezone

# Create your models here.

class News(models.Model):
	title_text = models.CharField(max_length = 20)
	context_text = models.CharField(default = '', max_length = 1000)
	pub_date = models.DateTimeField('date published')
	def __str__(self):
		return self.title_text