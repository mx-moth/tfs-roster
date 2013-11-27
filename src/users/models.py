import datetime
import re
import uuid

from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.core import validators
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils import timezone


PASSWORD_RESET_TIMEOUT = getattr(settings, 'USER_PASSWORD_RESET_TIMEOUT',
                                 datetime.timedelta(days=14))
PASSWORD_RESET_EMAIL_SLUG = getattr(settings, 'USER_PASSWORD_RESET_EMAIL_SLUG',
                                    'password reset')


class UserManager(BaseUserManager):

    def create_user(self, email, username=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, username and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The user must have a valid email address')
        email = UserManager.normalize_email(email)
        user = self.model(email=email, username=username,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, username=None, **extra_fields):
        u = self.create_user(email, username, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        _('username'), max_length=30, null=True, blank=True,
        help_text=_('Optional. 30 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'), _('Enter a valid username.'),
                'invalid')
        ])

    email = models.EmailField(_('email address'), unique=True, blank=False)

    first_name = models.CharField(_('first name'), max_length=255, blank=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True)

    is_staff = models.BooleanField(
        _('staff status'), default=False, help_text=_(
            'Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True, help_text=_(
        'Designates whether this user should be treated as active. Unselect '
        'this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __unicode__(self):
        if self.first_name or self.last_name:
            return '{0} {1}'.format(self.first_name, self.last_name).strip()
        elif self.username:
            return self.username
        else:
            return self.email

    def get_full_name(self):
        return unicode(self)

    def get_short_name(self):
        """ Produce a short name, depending upon which fields have data. This
            can produce names in the following format:

            * User N. - for {first_name: 'User', last_name: 'Name'}
            * User - for {first_name: 'User', last_name: ''}
            * Name - for {first_name: '', last_name: 'Name'}
            * username - for Users without a name, but with a username
            * user@example.com - for Users with no name or username
        """
        if self.first_name and self.last_name:
            return '{0} {1}.'.format(self.first_name, self.last_name[0])
        elif self.first_name or self.last_name:
            return self.first_name or self.last_name
        elif self.username:
            return self.username
        else:
            return self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = False

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])
