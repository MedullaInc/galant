from base import *

DATABASES = {
    'default': {
        'NAME': 'gallant',
        'ENGINE': 'django.db.backends.sqlite3',
        'OPTIONS': {
          'autocommit': True,
        },
    }
}
