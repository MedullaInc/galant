from gallant.settings.base import *

DATABASES = {
    'default': {
        'NAME': 'gallant_dev_broken',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': '',
        'OPTIONS': {
          'autocommit': True,
        },
    }
}
