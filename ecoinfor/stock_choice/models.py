# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

# Create your models here.
class Stock(models.Model):
    stockname = models.CharField(max_length=50, blank=True, null=True)
    stockcode = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock'

"""
class Stock(models.Model):
	name_text = models.CharField(max_length = 20)
	intro_text = models.CharField(max_length = 1000)
	company_text = models.CharField(max_length = 200)
	hot_index = models.IntegerField()
	
	def __str__(self):
		return self.name_text
		"""