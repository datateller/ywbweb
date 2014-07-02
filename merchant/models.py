from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, fromstr
from django.contrib.gis.measure import D
# Create your models here.

class Merchant(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    description = models.CharField(max_length=2000)
    point = models.PointField(null=True)
    objects = models.GeoManager()


class Commercial(models.Model):
    merchant = models.ForeignKey(Merchant)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=2000)
    photo = models.ImageField(upload_to='b_photos/%Y/%m/%d', max_length=10000000, blank=True, null=True, default='b_photos/default.jpg')


############################################################################

class Baby(models.Model):
    user = models.OneToOneField(User)
    type = models.IntegerField(10,null=True)   ###type = 1: from app, type =2: from weixin
    name = models.TextField(max_length=40,null=True)                                     
    birthday = models.DateField(null=True)
    sex = models.TextField(max_length=10,null=True)
    weight = models.FloatField(2,null=True)
    height = models.FloatField(2,null=True)
    city = models.TextField(max_length=40,null=True)
    homeaddr = models.TextField(max_length=100,null=True)
    schooladdr = models.TextField(max_length=100,null=True)
    homepoint = models.PointField(null=True)
    objects = models.GeoManager()

    class Meta:
        app_label="baby"

class CommercialHistory(models.Model):
    commercial_id = models.IntegerField()
    merchant_id = models.IntegerField()
    baby_id = models.IntegerField()
    
