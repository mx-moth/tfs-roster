from __future__ import absolute_import

from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import views

urlpatterns = patterns(
    '',
    url(r'^$',
        views.dashboard,
        name='dashboard'),
    url(r'^station/(?P<station_pk>\d+)/$',
        views.station_dashboard,
        name='station-dashboard'),
    url(r'^station/(?P<station_pk>\d+)/',
        include('schedules.urls')),
)
