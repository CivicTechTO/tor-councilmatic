# Toronto Councilmatic

[![Issues in HuBoard](https://img.shields.io/github/issues/civictechto/tor-councilmatic.svg?label=HuBoard)](https://huboard.com/CivicTechTO/tor-councilmatic#/?milestone=["Public Launch"])
[![HuBoard: Ready](https://img.shields.io/github/issues-raw/civictechto/tor-councilmatic/1 - Ready.svg?label=Ready)](https://huboard.com/CivicTechTO/tor-councilmatic#/?milestone=["Public Launch"])
[![HuBoard: Working](https://img.shields.io/github/issues-raw/civictechto/tor-councilmatic/2 - Working <= 5.svg?label=Working)](https://huboard.com/CivicTechTO/tor-councilmatic#/?milestone=["Public Launch"])
[![HuBoard: Review](https://img.shields.io/github/issues-raw/civictechto/tor-councilmatic/3 - Review.svg?label=Review)](https://huboard.com/CivicTechTO/tor-councilmatic#/?milestone=["Public Launch"])

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

After Vagrant and VirtualBox are installed, just run this from the
project root directory:

    vagrant up

Follow the instructions provided when the command completes.

It may take quite awhile the first time your run it, as several large
downloads will need to occur.

When you're done working, you can run the following command to free up
system resources:

    vagrant halt

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
If you plan on making changes to core councilmatic features (as opposed to Chicago-specific stuff), you'll want to install django-councilmatic locally instead of installing from pypi.

```bash
cd ..
git clone https://github.com/datamade/django-councilmatic.git
cd django-councilmatic
python setup.py develop
cd ../tor-councilmatic
```

## Importing data from the open civic data api

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

## Running Chicago Councilmatic locally

``` bash
inv django.run
```

Navigate to http://localhost:8000/

## Setup Search

**Install Open JDK or update Java**

On Ubuntu:

``` bash
$ sudo apt-get update
$ sudo apt-get install openjdk-7-jre-headless
```

On OS X:

1. Download latest Java from
[http://java.com/en/download/mac_download.jsp?locale=en](http://java.com/en/download/mac_download.jsp?locale=en)
2. Follow normal install procedure
3. Change system Java to use the version you just installed:

    ``` bash
    sudo mv /usr/bin/java /usr/bin/java16
    sudo ln -s /Library/Internet\ Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java /usr/bin/java
    ```

**Index the database**
```bash
python manage.py rebuild_index
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
