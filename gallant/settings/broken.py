from gallant.settings.base import *

# For testing on broken git branch, use different databse. Point DJANGO_SETTINGS_MODULE
# environment variable here when on broken.

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
