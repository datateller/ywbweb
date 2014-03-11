'''
Created on Nov 2, 2013

@author: shengeng
'''
from django.conf.urls import patterns, url

from knowledge import views

urlpatterns = patterns('',
    url(r'^getknowl/', views.getknowl, name='getknowl'),
    url(r'^getknowllist/', views.getknowllist, name='getknowllist'),
    url(r'^getknowlbyid/',views.getknowlbyid, name='getknowlbyid'),
    url(r'^collectknowl/',views.collectknowl, name='collectknowl'),
)