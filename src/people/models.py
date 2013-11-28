from chainablemanager import ChainableManager
from django.db import models
from django.db.models import Q
from django.db.models.sql.query import get_order_dir
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

        def successor_of(self, instance):
            return self.get_neighbour(instance, True)

        def predecessor_of(self, instance):
            return self.get_neighbour(instance, False)

        def get_neighbour(self, instance, successor=True):
            """
            Get the neighbour of an object in the queryset
            """

            # First, determine the ordering. This code is from get_ordering() in
            # django.db.sql.compiler
            if self.query.extra_order_by:
                ordering = self.query.extra_order_by
            elif not self.query.default_ordering:
                ordering = self.query.order_by
            else:
                ordering = self.query.order_by or self.query.model._meta.ordering

            assert '?' not in ordering, 'This makes no sense for random ordering.'

            # If we want the previous object, reverse the default ordering
            default_ordering = 'ASC' if successor else 'DESC'
            ordering_map = {'ASC': 'gt', 'DESC': 'lt'}

            # To find the sucessor, we need to construct a filter such that
            # (replacing greater with lesser as appropriate):
            #
            # * The first value is greater than the instance value, or
            # * The first value is the same, but the second is greater, or
            # * The first n-1 values are the same, but the nth value is greater
            #
            # ``q`` holds the final ``Q`` instance used for filtering, and is
            # built up each iteration. ``same_q`` holds a ``Q`` value used to
            # ensure the ``n-1`` previous values are the same for the ``nth``
            # field
            q = Q()
            same_q = Q()
            for field in ordering:
                item_value = reduce(getattr, field.split('__'), instance)
                field, direction = get_order_dir(field, default_ordering)
                condition = '{0}__{1}'.format(field, ordering_map[direction])

                q = q | (same_q & Q(**{condition: item_value}))
                same_q = same_q & Q(**{field: item_value})

            # Construct a new QuerySet to find the neighbour
            qs = self.filter(q)

            # Reverse the order if we're looking for the predecessor
            if not successor:
                qs = qs.reverse()

            # Return the neighbour, or None if it does not exist
            try:
                return qs[0]
            except IndexError:
                return None


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
