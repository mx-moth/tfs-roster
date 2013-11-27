from __future__ import absolute_import

from django import forms
from django.contrib import admin
from djangosuggestions.widgets import SuggestionWidget
from schedules.models import (Shift, Availability)
from utils.admin import register


@register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'start', 'end']


@register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    pass
