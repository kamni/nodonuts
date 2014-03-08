# NoDonuts

A stand-alone Django project that helps organizations and campaigns coordinate
bringing healthy food for events and ongoing meetups. The site provides support
for multiple organizations to share recipes on the same site. Organizations and
their members can add new recipes that can be searched and rated by other
users; organization staff can setup meetings and events, and members can sign
up to bring food to those events.

## NOTE:

Setup and configuration assumes that you are working on a *nix-based server.
Please adapt these instructions accordingly if you are working on a Windows
machine.

## Basic Installation

Clone the repository to the location on your server where you plan to host the
project:

    git clone https://github.com/kamni/nodonuts.git

Create a virtualenv outside of the project:

    virtualenv --no-site-packages venv
    . venv/bin/activate

Install the requirements:

    cd nodonuts
    pip install -r nodonuts/requirements.txt

If you are not planning to use sqlite (not recommended for larger sites), you
should install either postgres libraries

    pip install psycopg2

or mysql libraries

    pip install mysql-python

depending on which database you plan to use.

To configure Django settings, make a copy of `srv_settings.py.example` and
edit to fit your needs (see Django's own documentation regarding settings.py):

    cp nodonuts/srv_settings.py.example nodonuts/srv_settings.py
    vi nodonunts/srv_settings.py # or your editor of choice

Next, prepare static resources (css/js/images) for being served:

    python manage.py collectstatic

Sync your db:

    python manage.py syncdb

Finally, follow any additional instructions for setting up a Django project for
your particular web host or server. There is a `Procfile.sample` and a
`passenger_wsgi.py.sample` (for gunicorn and passenger, respectively) to get
you started.

## Django Constance Settings

## Search Configuration

This project uses django-haystack on top of Whoosh to run its search queries.
In order to run searches you must do the following:

1. Create recipes and tags using the Django admin or a (see the 'Default Data'
section for some auto-generated options).

2. Create a `whoosh_index` folder in the `nodonuts` directory:

    cd <path-to-nodonuts-project>
    mkdir nodonuts/whoosh_index

3. Generate the search indexes for the first time:

    python manage.py rebuild_index

These indexes will need to be updated whenever new recipes/tags are added or
recipes change.  You can do this manually by running:

    python manage.py update_index recipes

To automate this, you may consider creating a cron job on your server. Here is
an example entry:

    0 * * * *  cd <path to project> && <path to venv>/bin/python manage.py update_index recipes

### Configuration Note:

Whoosh relies on files for storing search indexes. While Whoosh3 may be
working toward database storage for indexes, this feature is not yet available
for django-haystack and this project.

This may cause issues on servers that lack persistant storage (Heroku) or
servers managed by puppet, because the search indexes may be wiped out
immediately after generating them.

### Advanced configuration: automated updates for search indexes using Celerybeat

Search index updates can be run just fine using a cron job. However, if your
host does not support custom cron jobs or you would like a more configurable
approach, you may also want to use Celerybeat.

Django-celery is an app that integrates the task queue library, Celery, with
Django. It has a sub-project, Celerybeat, that will run tasks periodically,
similar to cron jobs.

Celery/Celerybeat is included as part of this project, along with configuration
to run the `update_index` command once per hour. By default, django-celery uses
the database queue backend, which should be sufficient for most uses of this
site, but it can be configured to use several popular queueing systems,
including RabbitMQ and Redis.

You can change the default settings by uncommenting the Celery configuration
lines in `srv_settings.py.example` (assumed to be copied into your
`srv_settings.py`). For more information on configuration, please
[visit the Celery docs](http://celery.readthedocs.org/en/latest/django/index.html)
for more information. You may also want to read the
[section on brokers](http://docs.celeryproject.org/en/latest/getting-started/brokers/index.html).

Django-celery does not run by itself. For simple development use, you can run
the following command:

    python manage.py celerybeat

For production, celery should be daemonized. Celery has a
[tutorial on writing a daemon](http://celery.readthedocs.org/en/latest/tutorials/daemonizing.html?highlight=celerybeat%20daemon)
for celerybeat.

## Documentation

Documentation is located in the `docs` folder and uses django-sphinxdoc to
generate and display content. You should read more on [Sphinx](http://sphinx-doc.org/)
and [django-sphinxdoc](https://bitbucket.org/ssc/django-sphinxdoc) if you want
to modify any of the documentation.

The documentation is meant to be displayed online as part of the nodonuts web
app, but it doesn't display by default. To enable it, do the following:

1. Insert the fixture that points the db towards the nodonuts docs:

    python manage.py loaddata docs

2. Change the Sphinx configuration in `srv_settings.py` to make the urls
accessible:

    INCLUDE_DOC_URLS = True

This will make [http://<project_url>/docs/nodonuts/] accessible if you visit
the link directly, but it will not show up in the navigation bar as a link. If
you want anyone who visits the site to be able to find the docs easily, you
should also change:

    DISPLAY_DOC_LINKS = True

If INCLUDE_DOC_URLS is set to True, you can also update DISPLAY_DOC_LINKS
using the `Constance` configuration in the database.

3. Generate the docs (WARNING: this will also rebuild any of your recipe search
indexes, and will make the recipe search unavailable until the docs are
finished generating):

    python manage.py updatedoc -b nodonuts

This same step will need to be run again if the docs change.

## Default Data

The project does not have an initial_data fixture, in order to allow site
managers to customize their installations. However if you would like to install
some default data, there are some fixtures available:

Recipe Tags:

    python manage.py loaddata recipe_tags

You may also generate some nonsensical recipe and user data for the purposes of
testing. From the top-level project directory, run the following script:

    python tests/scripts/gnerate_data.py
