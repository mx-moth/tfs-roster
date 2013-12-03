from __future__ import absolute_import, unicode_literals

import datetime

from django import forms

from people.models import Person

from .models import Availability


class SelectPersonForm(forms.Form):

    person = forms.ModelChoiceField(Person.objects.all())

    def __init__(self, data=None, files=None, people=None, **kwargs):
        super(SelectPersonForm, self).__init__(data, files, **kwargs)
        if people is not None:
            self.fields['person'].queryset = people


class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ('start', 'end', 'availability', 'rostered', 'comments')

    def __init__(self, data=None, files=None, instance=None, person=None,
                 date=None, **kwargs):
        super(AvailabilityForm, self).__init__(
            data, files, instance=instance, **kwargs)
        self.person = person
        self.date = date

    def save(self, commit=True):
        instance = super(AvailabilityForm, self).save(commit=False)
        instance.person = self.person
        instance.date = self.date

        if commit:
            instance.save()

        return instance
