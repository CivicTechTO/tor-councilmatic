from invoke import run, task, Collection
import sys
import subprocess

import urllib.request
from urllib.error import URLError

ns = Collection()

@task(default=True)
def list_tasks():
    """Show tasks, basically an alias for --list.

    Needed as a default task due to https://github.com/pyinvoke/invoke/issues/180
    """
    run('invoke --list')

@task()
def check_venv():
    """Check whether virtualenv is being used"""
    if not hasattr(sys, 'real_prefix'):
        print('This project requires using virtualenv. Please activate it.')
        print('(See README for details.')
        sys.exit(1)
    else:
        print('Yay! You are properly using virtualenv. Continuing...')

ns.add_task(check_venv)
ns.add_task(list_tasks)

pip = Collection('pip')

@task(check_venv)
def pip_install():
    """Install pinned packages from requirements.lock"""
    run('pip install -r requirements.lock')

@task(check_venv)
def pip_update():
    """Update packages from requirements.unlocked.txt"""
    run('pip install --upgrade -r requirements.unlocked.txt')

@task(check_venv)
def pip_lock():
    """Lock packages into requirements.lock"""
    run('pip freeze > requirements.lock')

pip.add_task(pip_install, 'install')
pip.add_task(pip_update, 'update')
pip.add_task(pip_lock, 'lock')
ns.add_collection(pip)

django = Collection('django')

@task(check_venv)
def django_db_reset():
    """Reset the database & run migrations"""
    run('rm -f tor_councilmatic.db')
    run('./manage.py migrate --no-initial-data')

@task(check_venv)
def django_loaddata():
    """Load objects updated within the past 2 weeks"""
    cmd = 'date --date="2 weeks ago" "+%F"'
    proc = subprocess.popen(cmd, stdout=subprocess.PIPE)
    date = proc.stdout.read()
    run('./manage.py loaddata --update_since={} --endpoint=events'.format(date))
    run('./manage.py loaddata --update_since={} --endpoint=organizations'.format(date))
    run('./manage.py loaddata --update_since={} --endpoint=people'.format(date))
    run('./manage.py loaddata --update_since={} --endpoint=bills'.format(date))
    print(date)

@task(check_venv, help={'elasticsearch': 'Use local elasticsearch service. (Allows faceted search)'})
def django_run(elasticsearch=False):
    """Run a local server for Councilmatic"""
    cmd = 'gunicorn councilmatic.wsgi --log-file -'
    if elasticsearch:
        es_base = '127.0.0.1:9200'
        es_index = 'toronto'

        es_url = es_base + '/' + es_index
        try:
            urllib.request.urlopen('http://'+es_base)
            print('Yay! Elasticsearch appears to be running...')
        except URLError:
            raise ValueError("Elasticsearch not available at "+es_url)
        cmd = 'SEARCH_URL=elasticsearch://' + es_url + ' ' + cmd
    run(cmd)

django.add_task(django_db_reset, 'db_reset')
django.add_task(django_loaddata, 'loaddata')
django.add_task(django_run, 'run')
ns.add_collection(django)
