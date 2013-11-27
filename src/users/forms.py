from __future__ import unicode_literals

from django import forms
from django.forms.util import flatatt
from django.template import loader
from django.utils.datastructures import SortedDict
from django.utils.html import format_html, format_html_join
from django.utils.http import int_to_base36
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext, ugettext_lazy as _

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import UNUSABLE_PASSWORD, identify_hasher
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site


# A bunch of the default form bits are find to use as-is, so just import them
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField, ReadOnlyPasswordHashWidget, mask_password,
    AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm,
    AdminPasswordChangeForm
)


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'duplicate_email': _("A user with that email address already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }

    email = forms.EmailField(label=_("Email address"))

    username = forms.RegexField(
        label=_("Username"), max_length=30, required=False,
        regex=r'^[\w.@+-]+$',
        help_text=_("Optional. 30 characters or fewer. Letters, digits and "
                    "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    password1 = forms.CharField(
        label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_("Password confirmation"), widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = get_user_model()
        fields = ("email", "username",)

    def clean_email(self):
        email = self.cleaned_data["email"]
        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        UserModel = self._meta.model
        try:
            UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def clean_username(self):
        username = self.cleaned_data["username"]
        if not username:
            return None

        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        UserModel = self._meta.model
        try:
            UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    username = forms.RegexField(
        required=False, label=_("Username"), max_length=30,
        regex=r"^[\w.@+-]+$",
        help_text=_("Optional. 30 characters or fewer. Letters, digits and "
                    "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
    }

    class Meta:
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_username(self):
        username = self.cleaned_data["username"]
        if not username:
            return None

        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        UserModel = self._meta.model

        exists = UserModel.objects.filter(username=username)\
            .exclude(pk=self.instance.pk).exists()

        if not exists:
            return username

        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
