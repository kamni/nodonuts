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

    pip install -r nodonuts/requirements.txt

If you are not planning to use sqlite (not recommended for larger sites), you
should install either postgres libraries

    pip install psycopg2

or mysql libraries

    pip install mysql-python

depending on which database you plan to use.

To configure Django settings, make a copy of `srv_settings.py.example` and
edit to fit your needs (see Django's own documentation regarding settings.py):

    cd nodonuts/
    cp nodonuts/srv_settings.py.example nodonuts/srv_settings.py
    vi srv_settings.py # or your editor of choice

Next, prepare static resources (css/js/images) for being served:

    python manage.py collectstatic

Finally, follow any additional instructions for setting up a Django project for
your particular web host or server. There is a `Procfile.sample` and a
`passenger_wsgi.py.sample` (for gunicorn and passenger, respectively) to get
you started.

## Search Configuration

This project uses django-haystack on top of Whoosh to run its search queries.
In order to run searches you must do the following:

1. Create recipes and tags using the Django admin or a (see the 'Default Data'
section for some auto-generated options).

2. Create a `whoosh_index` folder in the `nodonuts` directory:

    cd <path-to-nodonuts-project>
    mkdir nodonuts/whoosh_index

3. Generate the search indexes:

    python manage.py rebuild_index

These indexes will need to be rebuilt whenever new recipes/tags are added or
recipes change.

## Default Data

The project does not have an initial_data fixture, in order to allow site
managers to customize their installations. However if you would like to install
some default data, there are some fixtures available:

Recipe Tags:

    python manage.py loaddata recipe_tags

You may also generate some nonsensical recipe and user data for the purposes of
testing. From the top-level project directory, run the following script:

    python tests/scripts/gnerate_data.py
