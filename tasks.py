from invoke import run, task, Collection
import sys
import subprocess

ns = Collection()

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

@task(check_venv)
def django_run():
    """Run simple server"""
    run('gunicorn councilmatic.wsgi --log-file -')

django.add_task(django_db_reset, 'db_reset')
django.add_task(django_loaddata, 'loaddata')
django.add_task(django_run, 'run')
ns.add_collection(django)
