from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ywbweb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', include('apphome.urls')),
    url(r'^apphome/', include('apphome.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^merchant/', include('merchant.urls')),
    url(r'^merchant/accounts/', include('registration.backends.default.urls')),
    url(r'^weixin/', include('weixin.urls')),
    url(r'^surrounding/', include('surrounding.urls')),
    url(r'^offline/', include('offline.urls')),
)

