from __future__ import absolute_import

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render, get_object_or_404

from .models import Station


@login_required
def dashboard(request):
    station_list = list(Station.objects.for_user(request.user))
    if len(station_list) == 1:
        return redirect(reverse('station-dashboard', kwargs={
            'station_pk': station_list[0].pk}))
    return render(request, 'people/dashboard.html', {
        'station_list': station_list})


@login_required
def station_dashboard(request, station_pk):
    station = get_object_or_404(Station.objects.for_user(request.user),
                                pk=station_pk)
    return render(request, 'people/station.html', {
        'station': station})
