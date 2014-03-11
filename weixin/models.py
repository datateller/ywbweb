from django.db import models

# Create your models here.

class Knowledge(models.Model):
    title = models.CharField(max_length=1000)
    keyword = models.CharField(max_length=1000)
    abstract = models.TextField(max_length=1000)
    content = models.TextField(max_length=50000)
    images = models.TextField(max_length=2000)
    min = models.IntegerField(10)
    max = models.IntegerField(10)
    apply_sex = models.TextField(10)

class WeixinUser(models.Model):
    openid = models.CharField(max_length=100)
    baby_birthday = models.DateTimeField(null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    precision = models.FloatField(null=True)
