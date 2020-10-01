# Toronto Councilmatic - An Amazing Project

[![Current Milestone in HuBoard](https://img.shields.io/badge/issues-see_current_milestone-cc0000.svg)](https://huboard.com/CivicTechTO/tor-councilmatic#/?milestone=["Public Launch"])
[![HuBoard: Ready](https://img.shields.io/github/issues-raw/civictechto/tor-councilmatic/1 - Ready.svg?label=ready)](https://huboard.com/CivicTechTO/tor-councilmatic#/?milestone=["Public Launch"])
[![HuBoard: In Progress](https://img.shields.io/github/issues-raw/civictechto/tor-councilmatic/2 - In Progress <= 5.svg?label=in progress)](https://huboard.com/CivicTechTO/tor-councilmatic#/?milestone=["Public Launch"])

Keep track of what Toronto City Council is doing.

Click the "HuBoard" button above to see the tasks that are part of our
current milestone.

## Getting Started

Setup instructions will vary, depending on whether you're using
[Windows](#windows) or [Mac/Linux](#mac--linux).

### Windows

We'll be running the app on a *virtual machine*. This is a simulated
Linux system running safely and temporarily on your workstation, which
we can use to run our app. When this virtual machine is running, it may
be fairly resource-intensive, and so you'll need a fairly powerful
workstation.

**Requirements:**

* [Vagrant](https://www.vagrantup.com/docs/installation/): For managing
  a *virtual machine* running Ubuntu Linux. This is a simulated Linux
system running safely and temporarily on your workstation.
* [VirtualBox](https://www.virtualbox.org/wiki/Downloads): For Vagrant, which needs it.

After Vagrant and VirtualBox are installed, you can optionally install
the `vagrant-cachier` plugin. This will make for speedier Vagrant runs
after the first one, as it will cache the many download files used in
preparing Vagrant's virtual machine:

    vagrant plugin install vagrant-cachier

Then, just run this from the project root directory:

    vagrant up

Follow the instructions provided when the command completes. (Hint:
`vagrant ssh` will get you started.)

It may take quite awhile the first time your run it, as several large
downloads will need to occur.

When you're done working, you can run the following command to free up
system resources:

    vagrant halt

If you no longer plan to use Vagrant to develop for `tor-councilmatic`,
be sure to use this to free up disk space:

    vagrant destroy

You can find more details on using Vagrant
[here](https://www.vagrantup.com/docs/getting-started/teardown.html).

### Mac / Linux

We'll be running the app directly on your workstation. You won't need a
powerful system for this approach. (Yay!)

**Requirements:**

* [Install **Python 3.**.](http://www.tutorialspoint.com/python/python_environment.htm)
* [Install **SQLite3**.](http://mislav.net/rails/install-sqlite3/) For our
  development database.
* [`virtualenv`](http://virtualenv.readthedocs.org/en/latest/virtualenv.html): For sandboxing our python packages.
* [`virtualenvwrapper`](http://virtualenvwrapper.readthedocs.org/en/latest/install.html): For helping us manage `virtualenv`.

View descriptions of all the helper tasks by running the bare `invoke`
command in the project root directory.

[Read how to set up virtualenv.](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

Once you have `virtualenv` and `virtualenvwrapper` set up:

```bash
mkvirtualenv tor-councilmatic --python=$(which python3)
pip install invoke==0.12.2
git clone https://github.com/civictechto/tor-councilmatic.git
cd tor-councilmatic
inv pip.install
```

Afterwards, whenever you want to use this virtual environment to work on
tor-councilmatic, run:

```bash
workon tor-councilmatic
```

To set up the SQLite database:

```bash
inv django.db_reset
```

You can re-run that command to wipe the database and start fresh.


**OPTIONAL: install django-councilmatic locally**
If you plan on making changes to core councilmatic features (as opposed to Toronto-specific stuff), you'll want to install django-councilmatic locally instead of installing from pypi.

```bash
cd ..
git clone https://github.com/datamade/django-councilmatic.git
cd django-councilmatic
python setup.py develop
cd ../tor-councilmatic
```

## Importing data....

There are two ways to get up and running locally with a database:

**1. from a pre-generated development database**

Download the latest `tor_councilmatic.db` from the [releases
page](https://github.com/tor-councilmatic/tor-councilmatic/releases),
and place it in the project root directory.

**2. from the open civic data api**

The following invoke task will run the `loaddata` management command under
the hood. By default, it's pulling data from Toronto's OCD API endpoint
at [toronto-ocd-api.herokuapp.com][] (This may take a while, depending
on volume of data.)

```bash
inv django.loaddata
```

By default, the loaddata command is smart about what it looks at on the
OCD API. If you already have bills loaded, it won't look at everything
on the API - it'll look at the most recently updated bill in your
database, see when that bill was last updated on the OCD API, & then
look through everything on the API that was updated after that point. If
you'd like to load things that are older than what you currently have
loaded, you can run the loaddata management command with a `--delete`
option, which removes everything from your database before loading.

The loaddata command has some more nuance than the description above,
for the different types of data it loads. If you have any questions,
open up an issue and pester us to write better documentation.

## Running Toronto Councilmatic locally

``` bash
inv django.run
```

Navigate to http://localhost:8000/

## Setup Elasticsearch

Haystack is a python package that helps us provide search in our app. It
can use many different search backends. We use a powerful search backend
service called "Elasticsearch" in staging and production. However, in
order to make local development easier, we default to using a "Simple
Search" backend. It works well, but does not allow for [faceted
search](https://stackoverflow.com/questions/5321595/what-is-faceted-search)
features.

To enable faceted search features for local testing, you'll need to
[install
Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/_installation.html).

Once installed and running, assuming you've already run through the
`loaddata` process, you'll need to index the database:

```bash
./manage.py rebuild_index
```

You can then run Councilmatic using Elasticsearch like so:

```
inv django.run --elasticsearch
```

## Team

* David Moore - project manager
* Forest Gregg - Open Civic Data (OCD) and Legistar scraping
* Cathy Deng - data models and loading
* Derek Eder - front end
* Eric van Zanten - search and dev ops

## Errors / Bugs

If something is not behaving intuitively, it is a bug, and should be reported.
Report it here: https://github.com/datamade/chi-councilmatic/issues

## Note on Patches/Pull Requests

* Fork the project.
* Make your feature addition or bug fix.
* Commit, do not mess with rakefile, version, or history.
* Send a pull request. Bonus points for topic branches.

## Copyright

Copyright (c) 2015 Participatory Politics Foundation and DataMade. Released under the [MIT License](https://github.com/datamade/chi-councilmatic/blob/master/LICENSE).
