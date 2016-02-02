from gallant.settings.base import *

os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = "localhost:8001-8010,9200-9300"

DATABASES = {
    'default': {
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
