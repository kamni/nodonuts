# NoDonuts

A stand-alone Django project that helps organizations and campaigns coordinate
bringing healthy food for events and ongoing meetups. The site provides support
for multiple organizations to share recipes on the same site. Organizations and
their members can add new recipes that can be searched and rated by other
users; organization staff can setup meetings and events, and members can sign
up to bring food to those events.

## Heroku Installation

This project is already configured to run on Heroku. Simply create a Heroku app
and clone it. Then:

    git remote add origin https://github.com/kamni/nodonuts.git
    git push origin master

If you want to customize any of the django settings (found in
`nodonuts/settings.py`), please create a `srv_settings.py` file in
the `nodonuts` folder and override any settings there.

## Configuration

Configuration assumes that you are working on a *nix-based server. Please adapt
these instructions accordingly if you are working on a Windows machine.

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
