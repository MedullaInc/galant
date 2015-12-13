from gallant.settings.base import *

DATABASES = {
    'default': {
        'NAME': 'gallant_dev',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': '',
        'OPTIONS': {
          'autocommit': True,
        },
    }
}

# disable email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'