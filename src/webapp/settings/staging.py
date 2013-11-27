# staging environment
from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': path.join(VAR_ROOT, 'db.sqlite3'),
    }
}

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ID = 2

try:
    from .local import *
except ImportError:
    pass

