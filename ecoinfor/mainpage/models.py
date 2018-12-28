from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


# Be careful! In 'INSTALLED_APPS' at setting.py
# There is an APP called 'contrib.messages'!
# Later recommend that we should use class 'Information' instead


class News(models.Model):
    title = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=80, blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    topic = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=50, blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    keystock = models.TextField(blank=True, null=True)
    senti = models.IntegerField(blank=True, null=True)
    senti1 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news'


class TempNews(models.Model):
    title = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=80, blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    keystock = models.TextField(blank=True, null=True)
    senti = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'temp_news'