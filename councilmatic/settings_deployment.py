# These are all the settings that are specific to a deployment

import os
from configurations.values import BooleanValue, DatabaseURLValue, SearchURLValue, CacheURLValue, Value

class DeploymentConfig(object):
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'replacethiswithsomethingsecret'

    # SECURITY WARNING: don't run with debug turned on in production!
    # Set this to True while you are developing
    DEBUG = BooleanValue(True)

    POLIS_SITE_ID = Value(None)

    # Unrestricted staging key (disposable)
    GMAPS_API_KEY = Value('AIzaSyDVJdClcbq1ioJUeySpPgNiDndQEspN6Ck')
    # Set this to a "frozen version" in production
    # See: https://developers.google.com/maps/documentation/javascript/versions#the-frozen-version
    GMAPS_API_VERSION = Value('3.exp')

    # See: https://django-configurations.readthedocs.org/en/stable/values/#configurations.values.DatabaseURLValue
    DATABASES = DatabaseURLValue('sqlite:///tor_councilmatic.db')

    # See: https://django-configurations.readthedocs.org/en/stable/values/#configurations.values.SearchURLValue
    # See: https://github.com/dstufft/dj-search-url
    HAYSTACK_CONNECTIONS = SearchURLValue('simple://')

    # See: https://django-configurations.readthedocs.org/en/stable/values/#configurations.values.CacheURLValue
    # See: https://github.com/ghickman/django-cache-url
    CACHES = CacheURLValue('dummy://')

    # Set this to flush the cache at /flush-cache/{FLUSH_KEY}
    FLUSH_KEY = 'super secret junk'

    # Set this to allow Disqus comments to render
    DISQUS_SHORTNAME = None

    # analytics tracking code
    ANALYTICS_TRACKING_CODE = Value('')

    HEADSHOT_PATH = os.path.join(os.path.dirname(__file__), '..'
                                 '/toronto/static/images/')

    EXTRA_APPS = ()
