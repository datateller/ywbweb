from django.db import models
from django.contrib.gis.db import models

# Create your models here.

class Shop(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    url = models.CharField(max_length=1000)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    point = models.PointField()
    objects = models.GeoManager()