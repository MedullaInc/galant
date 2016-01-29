from gallant.settings.base import *

os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = "localhost:8001-8010,9200-9300"

DATABASES = {
    'default': {
        'NAME': ':memory:',
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

MIGRATION_MODULES = {
    'gallant': None,
    'quotes': None,
    'briefs': None,
    'calendr': None,
}