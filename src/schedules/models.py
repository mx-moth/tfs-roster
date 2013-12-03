import datetime

from chainablemanager import ChainableManager

from django.db import models


class Shift(models.Model):
    station = models.ForeignKey('people.Station', related_name='shifts')

    nickname = models.CharField(max_length=50)

    start = models.TimeField()
    end = models.TimeField()

    class Meta(object):
        ordering = ('station', 'start')

    def __unicode__(self):
        return '{0} - {1}'.format(self.start, self.end)

    def start_from_date(self, date):
        return datetime.datetime.combine(
            date=date,
            time=self.start)

    def end_from_date(self, date):
        if self.start > self.end:
            date = date + datetime.timedelta(days=1)

        return datetime.datetime.combine(
            date=date,
            time=self.end)


class AvailabilityManager(ChainableManager):
    class QuerySetMixin(object):
        pass

    def for_dates(self, person, dates):
        schedule = {s.date: s
                    for s in self.filter(person=person, date__in=dates)}

        for date in dates:
            if date in schedule:
                yield schedule[date]
            else:
                yield self.model(date=date, person=person)


class Availability(models.Model):
    person = models.ForeignKey('people.Person', related_name='schedule')

    date = models.DateField()

    start = models.TimeField()
    end = models.TimeField()

    STATUS_UNAVAILABLE = 'unavailable'
    STATUS_WORKING = 'working'
    STATUS_AVAILABLE = 'available'
    STATUS_REST_DAY = 'rest'
    STATUS_ROSTERED = 'rostered'
    STATUS_CSS_CLASSES = {
        STATUS_UNAVAILABLE: 'danger',
        STATUS_WORKING: 'warning',
        STATUS_AVAILABLE: 'success',
        STATUS_REST_DAY: 'warning',
        STATUS_ROSTERED: 'info',
    }
    AVAILABILITY_CHOICES = (
        (STATUS_UNAVAILABLE, 'Unavailable'),
        (STATUS_WORKING, 'Working, but available'),
        (STATUS_AVAILABLE, 'Available'),
        (STATUS_REST_DAY, 'Rest day'),
    )
    availability = models.CharField(max_length=15, choices=AVAILABILITY_CHOICES)
    rostered = models.BooleanField(default=False)

    truck = models.ForeignKey('people.Truck', null=True, blank=True)

    comments = models.TextField(blank=True)

    objects = AvailabilityManager()

    class Meta(object):
        ordering = ('date', 'start', '-rostered', 'availability')
        verbose_name_plural = 'schedule'

    def __unicode__(self):
        return '{person} - {date} {start} till {end}: {status}'.format(
            person=self.person,
            date=self.date,
            start=self.start,
            end=self.end,
            status=self.get_status_display())

    @property
    def status(self):
        return self.STATUS_ROSTERED if self.rostered else self.availability

    def get_status_class(self):
        """Get a CSS class appropriate for the status"""
        status = self.STATUS_ROSTERED if self.rostered else self.status
        return self.STATUS_CSS_CLASSES.get(status, '')

    def get_status_display(self):
        if self.rostered:
            return 'Rostered'
        else:
            return self.get_availability_display()
