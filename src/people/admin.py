from django import forms
from django.contrib import admin
from djangosuggestions.widgets import SuggestionWidget
from people.models import (
    Station, Truck, Person, Rank, Qualification, PhoneNumber)
from schedules.models import Shift
from utils.admin import register


@register(Station)
class StationAdmin(admin.ModelAdmin):
    class TruckInline(admin.TabularInline):
        model = Truck
        extra = 1

    class ShiftInline(admin.TabularInline):
        model = Shift
        extra = 1

    inlines = [TruckInline, ShiftInline]

    list_display = ('name',)
    list_search = ('name',)


@register(Rank)
class RankAdmin(admin.ModelAdmin):
    pass


@register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    pass


@register(Person)
class PersonAdmin(admin.ModelAdmin):
    class PhoneNumberInline(admin.TabularInline):
        class PhoneNumberForm(forms.ModelForm):
            class Meta:
                widgets = {
                    'type': SuggestionWidget(
                        suggestions=PhoneNumber.TYPE_SUGGESTIONS),
                }

        model = PhoneNumber
        form = PhoneNumberForm
        extra = 1

    inlines = [PhoneNumberInline]

    filter_horizontal = ('qualifications',)

    list_display = ('name', 'rank', 'station')
    list_search = ('name')

    list_filter = ('rank', 'station')
