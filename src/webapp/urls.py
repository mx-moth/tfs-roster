from django.conf.urls import patterns, include, url
from django.contrib import admin

import webapp.views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^', include('people.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
