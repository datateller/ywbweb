from django.db import models
from django.contrib.gis.db import models
# Create your models here.

class MerchantLocation(models.Model):
    point = models.PointField()
    objects = models.GeoManager()

class EndUserLocation(models.Model):
    point = models.PointField()
    objects = models.GeoManager()
