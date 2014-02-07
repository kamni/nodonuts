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
`django_config/settings.py`), please create a `srv_settings.py` file in
the `django_config` folder and override any settings there.
