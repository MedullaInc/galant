from gallant.settings.base import *

os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = "localhost:8000-8010,8080,9200-9300"

DATABASES = {
    'default': {
        'NAME': 'gallant.sqlite3',
        'ENGINE': 'django.db.backends.sqlite3',
    },
}