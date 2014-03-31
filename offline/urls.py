'''
Created on Nov 2, 2013

@author: shengeng
'''
from django.conf.urls import patterns, url

from offline import views

urlpatterns = patterns('',
    url(r'^getoffline/([0-9]*)/$', views.offline_web_view),
    url(r'^addshop/', views.ShopFormView.as_view(success_url='/offline/addshop/')),
)