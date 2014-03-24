from django.test import TestCase

# Create your tests here.

from django.contrib.gis.measure import D
from django.test import TestCase

class SurroundingTest(TestCase):

    def get_names(self, qs):
        city = 'test city'
        print(city)
        return city
