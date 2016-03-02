# These are all the settings that are specific to a deployment

import os
import dj_database_url

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'replacethiswithsomethingsecret'

# SECURITY WARNING: don't run with debug turned on in production!
# Set this to True while you are developing
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tor_councilmatic',
        'USER': 'tor_councilmatic',
        'PASSWORD': '',
    }
}

# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        #'URL': 'http://127.0.0.1:8983/solr'
        # ...or for multicore...
        'URL': 'http://127.0.0.1:8983/solr/chicago',
    },
}

# Remember to run python manage.py createcachetable so this will work! 
# developers, set your BACKEND to 'django.core.cache.backends.dummy.DummyCache'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': 'councilmatic_cache',
    }
}

# Set this to flush the cache at /flush-cache/{FLUSH_KEY}
FLUSH_KEY = 'super secret junk'

# Set this to allow Disqus comments to render
DISQUS_SHORTNAME = None

# analytics tracking code
ANALYTICS_TRACKING_CODE = ''

HEADSHOT_PATH = os.path.join(os.path.dirname(__file__), '..'
                             '/chicago/static/images/')

EXTRA_APPS = ()
