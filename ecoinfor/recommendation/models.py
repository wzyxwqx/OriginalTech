from django.db import models
from django.utils import timezone

# Create your models here.
class News(models.Model):
    title_text = models.CharField(max_length = 20)
    context_text = models.CharField(default = '', max_length = 1000)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.title_text

# recommandation data
class RecomandStock(models.Model):
    time = models.DateTimeField(blank=True, null=True)
    stockcode = models.CharField(max_length=20, blank=True, null=True)
    pchange_1 = models.FloatField(blank=True, null=True)
    pchange_2 = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recomand_stock'


""" 实际要用这一个，那么views和urls都要改变量
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
        """