from chainablemanager import ChainableManager
from django.db import models
from django_localflavor_au.models import AUPhoneNumberField
from djangosuggestions.models import SuggestionField
from featureditem.fields import FeaturedField
from positions import PositionField


class StationManager(ChainableManager):
    class QuerySetMixin(object):
        def for_user(self, user):
            return self.all()  # TODO Filter this properly


class Station(models.Model):
    name = models.CharField(max_length=255)

    objects = StationManager()

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Truck(models.Model):
    station = models.ForeignKey('people.Station')
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Rank(models.Model):
    name = models.CharField(max_length=50)
    class_name = models.SlugField(max_length=50)
    order = PositionField()

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return self.name


class Qualification(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    class_name = models.SlugField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class PersonManager(ChainableManager):
    class QuerySetMixin(object):
        def current(self):
            return self.all()  # TODO filter this properly


class Person(models.Model):
    name = models.CharField(max_length=255)
    station = models.ForeignKey(Station, related_name='people')

    rank = models.ForeignKey(Rank)
    qualifications = models.ManyToManyField(Qualification, blank=True)

    objects = PersonManager()

    class Meta:
        ordering = ('rank__order', 'name',)
        verbose_name_plural = 'people'

    def __unicode__(self):
        return self.name


class PhoneNumber(models.Model):
    person = models.ForeignKey(Person, related_name='phone_numbers')

    TYPE_SUGGESTIONS = ('Mobile', 'Home', 'Work')
    type = SuggestionField(max_length=50, suggestions=TYPE_SUGGESTIONS)
    number = AUPhoneNumberField(default_area_code='03')
    primary = FeaturedField()

    class Meta:
        ordering = ('-primary',)

    def __unicode__(self):
        return '{0}: {1}'.format(self.type, self.number)
