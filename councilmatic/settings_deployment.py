# These are all the settings that are specific to a deployment

import os
from configurations import values

class DeploymentConfig(object):
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'replacethiswithsomethingsecret'

    # SECURITY WARNING: don't run with debug turned on in production!
    # Set this to True while you are developing
    DEBUG = values.BooleanValue(True)

    # See: https://django-configurations.readthedocs.org/en/stable/values/#configurations.values.DatabaseURLValue
    DATABASES = values.DatabaseURLValue('postgres://tor_councilmatic@localhost/tor_councilmatic')

    # See: https://django-configurations.readthedocs.org/en/stable/values/#configurations.values.SearchURLValue
    # See: https://github.com/dstufft/dj-search-url
    HAYSTACK_CONNECTIONS = values.SearchURLValue('elasticsearch://127.0.0.1:9200/toronto')

    # See: https://django-configurations.readthedocs.org/en/stable/values/#configurations.values.CacheURLValue
    # See: https://github.com/ghickman/django-cache-url
    CACHES = values.CacheURLValue('dummy://')

    # Set this to flush the cache at /flush-cache/{FLUSH_KEY}
    FLUSH_KEY = 'super secret junk'

    # Set this to allow Disqus comments to render
    DISQUS_SHORTNAME = None

    # analytics tracking code
    ANALYTICS_TRACKING_CODE = ''

    HEADSHOT_PATH = os.path.join(os.path.dirname(__file__), '..'
                                 '/chicago/static/images/')

    EXTRA_APPS = ()
