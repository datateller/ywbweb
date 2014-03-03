'''
Created on Nov 2, 2013

@author: shengeng
'''
from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns('',
    url(r'^login/', login_view),
    url(r'^logout/', logout_view),
    url(r'^$', MerchantMainPageView.as_view(), name='merchant_mainpage'),
    url(r'^register/', RegisterView.as_view(success_url='/merchant/'), name='register'),
    url(r'^home/', MerchantHomeView.as_view(), name='merchant_home'),
    url(r'^commercials/post/', CommercialPostView.as_view(success_url='/merchant/commercials/list/'), name='commercials_post'),
    url(r'^commercials/list/', CommercialListView.as_view(), name='commercials_list'),
    url(r'^commercials/', CommercialListView.as_view(), name='commercials'),
)

