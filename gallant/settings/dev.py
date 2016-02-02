from gallant.settings.base import *

DATABASES = {
    'default': {
    	'HOST': "127.0.0.1",
        'NAME': 'gallant_dev',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': '',
        'OPTIONS': {
          'autocommit': True,
        },
        'ATOMIC_REQUESTS': True,
    }
}

# disable email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'