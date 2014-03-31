'''
Created on 2013年12月31日

@author: shengeng
'''

from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User 

class ShopForm(forms.Form):
    name = forms.CharField()
    city = forms.CharField()
    address = forms.CharField()
    description = forms.CharField()
    url = forms.CharField()


    