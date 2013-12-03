from __future__ import absolute_import

from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import views

urlpatterns = patterns(
    '',

    url(r'^set/$',
        views.pick_person,
        name='set-schedule'),

    url(r'^set/(?P<person_pk>\d+)/$',
        views.set_schedule_for_person,
        name='set-schedule-for-person'),

    url(r'^toggle-rostered/(?P<person_pk>\d+)/(?P<availability_pk>\d+)$',
        views.toggle_rostered,
        name='toggle-rostered'),

    url(r'^view/$',
        views.view_schedule,
        name='view-schedule'),
)
