'''
Created on 2013年12月31日

@author: shengeng
'''

from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User 

class UserForm(forms.Form):
    longitude = forms.CharField()
    latitude = forms.CharField()
    
class MerchantLocationForm(forms.Form):
    longitude = forms.CharField()
    latitude = forms.CharField()
    