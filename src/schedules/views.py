import datetime

from contextlib import contextmanager
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render, redirect

from people.models import Station, Person

from .forms import SelectPersonForm, AvailabilityForm, UpdateAvailabilityForm
from .models import Availability
from .utils import daterange


@contextmanager
def ignored(*errors):
    try:
        yield
    except errors as err:
        pass


def parse_date_or_today(value):
    try:
        week_start_datetime = datetime.datetime.strptime(value, '%Y-%m-%d')
        return week_start_datetime.date()
    except ValueError:
        return datetime.date.today()


@login_required
def pick_person(request, station_pk):
    station = get_object_or_404(Station, pk=station_pk)
    return render(request, 'schedules/set/person.html', {
        'station': station})


@login_required
def set_schedule_for_person(request, station_pk, person_pk):
    station = get_object_or_404(Station, pk=station_pk)
    person = get_object_or_404(station.people.current(), pk=person_pk)

    week_start = parse_date_or_today(request.GET.get('week_start', ''))
    week_end = week_start + datetime.timedelta(days=6)
    next_week = week_start + datetime.timedelta(days=7)
    previous_week = week_start - datetime.timedelta(days=7)

    dates = list(daterange(week_start, next_week))
    schedule = Availability.objects.filter(person=person,
                                           date__range=(week_start, next_week))
    schedule_dict = {a.date: a for a in schedule}

    schedule_forms = [AvailabilityForm(data=request.POST or None,
                                       date=date, person=person,
                                       instance=schedule_dict.get(date, None),
                                       prefix='date_' + date.isoformat())
                      for date in dates]

    next_person = station.people.current().successor_of(person)

    if request.method == 'POST':
        changed_forms = [form for form in schedule_forms if form.has_changed()]
        if all(form.is_valid() for form in changed_forms):
            new_schedule = [form.save() for form in changed_forms]
            messages.success(request,
                             "{0}'s schedule for {1} - {2} has been set".format(
                                 person, week_start, week_end))
            next_action = request.POST.get('next-action', None)
            if next_action == 'next-person' and next_person:
                return redirect(reverse(set_schedule_for_person, kwargs={
                    'station_pk': station_pk,
                    'person_pk': next_person.pk}))
            return redirect(reverse(pick_person, kwargs={
                'station_pk': station_pk}))

    return render(request, 'schedules/set/times.html', {
        'week_start': week_start,
        'week_end': week_end,
        'previous_week': previous_week,
        'next_week': next_week,
        'schedule_forms': schedule_forms,
        'available_status': Availability.STATUS_AVAILABLE,
        'person': person,
        'station': station,
        'next_person': next_person})


@login_required
def update_availability(request, station_pk, person_pk, availability_pk):
    station = get_object_or_404(Station, pk=station_pk)
    person = get_object_or_404(station.people.current(), pk=person_pk)
    availability = get_object_or_404(person.schedule, pk=availability_pk)

    update_availability_form = UpdateAvailabilityForm(
        data=request.POST or None,
        instance=availability)

    if request.method == 'POST':
        if update_availability_form.is_valid():
            update_availability_form.save()
            return render(request, 'schedules/update_availability_done.html')

    return render(request, 'schedules/update_availability.html', {
        'station': station,
        'person': person,
        'availability': availability,
        'update_form': update_availability_form})


@login_required
def view_schedule(request, station_pk):
    station = get_object_or_404(
        Station.objects.prefetch_related('people', 'people__schedule'),
        pk=station_pk)

    week_start = parse_date_or_today(request.GET.get('week_start', ''))
    week_end = week_start + datetime.timedelta(days=6)
    next_week = week_start + datetime.timedelta(days=7)
    previous_week = week_start - datetime.timedelta(days=7)

    return render(request, 'schedules/view.html', {
        'week_start': week_start,
        'week_end': week_end,
        'week_range': list(daterange(week_start, next_week)),
        'previous_week': previous_week,
        'next_week': next_week,
        'station': station,
        'availability_statuses': dict(Availability.STATUS_CHOICES),
        'availability_classes': dict(Availability.STATUS_CSS_CLASSES)})
