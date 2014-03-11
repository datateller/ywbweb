from django.conf.urls import patterns, include, url

from django.contrib import admin
from .views import *
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ywbweb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^dev/', weixin_dev_view),
    url(r'^knowledge/([0-9]*)/$', weixin_knowledge_view),
)

