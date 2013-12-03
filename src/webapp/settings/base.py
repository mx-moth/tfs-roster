# Django settings for webapp project.
from os import path
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

# Path setup:
# / - Project root - PROJECT_ROOT
#   conf/ - System configuration - CONF_ROOT
#   src/ - The project source code - SRC_ROOT
#   var/ - Variable, non-version-controlled stuff - VAR_ROOT
#       logs/ - Log files - LOG_ROOT
#       tmp/ - Temporary files, cache, etc - TMP_ROOT
#       www/ - Web accessible content - WWW_ROOT
#           static/ - Static files - STATIC_ROOT
#           media/ - User uploaded content - MEDIA_ROOT

WEBAPP_ROOT = path.dirname(path.dirname(__file__))
SRC_ROOT = path.dirname(WEBAPP_ROOT)
PROJECT_ROOT = path.dirname(SRC_ROOT)

CONF_ROOT = path.join(PROJECT_ROOT, 'conf')
VAR_ROOT = path.join(PROJECT_ROOT, 'var')

CONF_ROOT = path.join(VAR_ROOT, 'logs')
TMP_ROOT = path.join(VAR_ROOT, 'tmp')

WWW_ROOT = path.join(VAR_ROOT, 'www')
STATIC_ROOT = path.join(WWW_ROOT, 'static')
MEDIA_ROOT = path.join(WWW_ROOT, 'media')


# URL structure
WWW_URL = '/assets/'
MEDIA_URL = path.join(WWW_URL, 'media/')
STATIC_URL = path.join(WWW_URL, 'static/')


INSTALLED_APPS = (
    # Apps from this project
    'webapp',
    'users',
    'people',
    'schedules',

    # Third party apps
    'adminextensions',
    'django_template_media',
    'jquery',
    'bootstrap3',
    'south',

    # Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'jquery.context_processors.jquery',
    'django_template_media.context_processors.template_media',
)


# Root project files
BASE_APP_NAME = 'webapp'
ROOT_URLCONF = '{}.urls'.format(BASE_APP_NAME)
WSGI_APPLICATION = '{}.wsgi.application'.format(BASE_APP_NAME)


# Built in Australia. Change this in local.py if you want it different
TIME_ZONE = 'Australia/Hobart'
LANGUAGE_CODE = 'en-au'


# Get set up for localisation
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Put all static files and templates in apps
STATICFILES_FINDERS = ['django.contrib.staticfiles.finders.AppDirectoriesFinder']
TEMPLATE_LOADERS = ['django.template.loaders.app_directories.Loader']


AUTH_USER_MODEL = 'users.User'


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


DATE_FORMAT = '%Y-%m-%d'


from django.contrib import messages
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}
