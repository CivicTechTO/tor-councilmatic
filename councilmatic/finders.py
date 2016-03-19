import hashlib
import logging
import os
import psycopg2
import psycopg2.extras
try:
    from urllib.request import urlopen
except ImportError:  # Python 2
    from urllib2 import urlopen

from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.finders import BaseFinder
from django.contrib.staticfiles.utils import matches_patterns
from django.conf import settings

logger = logging.getLogger(__name__)


class _ResourceInfo(object):
    hash_verified = False

    def __init__(self, url):
        self.url = url


class PersonHeadshotFinder(BaseFinder):
    def __init__(self):
        self.cache_dir = getattr(settings, "REMOTE_FINDER_CACHE_DIR", None)
        db_conn = settings.DATABASES['default']
        self.db_conn_kwargs = {
            'database': db_conn['NAME'],
            'user': db_conn['USER'],
            'password': db_conn['PASSWORD'],
            'host': db_conn['HOST'],
            'port': db_conn['PORT'],
        }

        if not self.cache_dir:
            raise ImproperlyConfigured("settings.REMOTE_FINDER_CACHE_DIR must point to a cache directory.")
        self.storage = FileSystemStorage(self.cache_dir)
        try:
            resources_setting = list(self.resources_from_db())
        except AttributeError:
            logger.warning("RemoteFinder is enabled, but settings.REMOTE_FINDER_RESOURCES is not defined.")
            resources_setting = ()
        if not isinstance(resources_setting, (list, tuple)):
            raise ImproperlyConfigured("settings.REMOTE_FINDER_RESOURCES must be a list or tuple")
        resources = {}
        for resource in resources_setting:
            try:
                path, url = resource
            except ValueError:
                raise ImproperlyConfigured("Each item in settings.REMOTE_FINDER_RESOURCES must be a tuple of two elements (path, url).")
            resources[path] = _ResourceInfo(url)
        self.resources = resources

    def resources_from_db(self):
        with psycopg2.connect(**self.db_conn_kwargs) as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
                curs.execute('SELECT * from councilmatic_core_person;')
                people = curs.fetchall()
                for p in people:
                    yield (os.path.join('images', 'headshots', p['slug'] + '.jpg'), p['headshot'])

    def find(self, path, all=False):
        try:
            resource_info = self.resources[path]
        except KeyError:
            return []
        self.fetch(path, resource_info)
        match = self.storage.path(path)
        if all:
            return [match]
        else:
            return match

    def fetch(self, path, resource_info):
        # delete from storage and re-download the file
        logger.info("Deleting %s from storage", path)

        # The following line does /not/ raise an exception if the file is
        # already deleted, which is desirable for us as it prevents an
        # error in the case of a race condition.
        self.storage.delete(path)

        # download the file
        logger.info("Downloading %s", resource_info.url)
        f = urlopen(resource_info.url)
        try:
            content = f.read()
        finally:
            f.close()

        # save it
        name = self.storage.save(path, ContentFile(content))
        if name != path:
            logger.warning("Save failed: %r != %r", name, path)

    def list(self, ignore_patterns):
        for path, resource_info in self.resources.items():
            if matches_patterns(path, ignore_patterns):
                continue
            self.fetch(path, resource_info)
            yield path, self.storage
