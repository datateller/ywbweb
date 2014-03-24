from django.conf.urls import patterns, include, url

from django.contrib import admin
from .views import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'geotest.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^adduser/', UserFormView.as_view(success_url='/surrounding/adduser/')),
    url(r'^addmerchant/',  MerchantLocationFormView.as_view(success_url='/surrounding/addmerchant/')),
    url(r'^map/',  MapView.as_view()),
    url(r'^getsurr/', surrounding_view),
)
