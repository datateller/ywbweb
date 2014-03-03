from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Merchant(models.Model):
    user = models.OneToOneField(User)
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    description = models.CharField(max_length=2000)


class Commercial(models.Model):
    merchant = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=2000)
    photo = models.ImageField(upload_to='b_photos/%Y/%m/%d', max_length=10000000, blank=True, null=True, default='b_photos/default.jpg')