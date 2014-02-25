"""
WSGI config for community_plate project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import os
import sys

PYTHON_VERSION = "python%s" % (sys.version[0:3])
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nodonuts.settings")
sys.path.insert(1, os.path.join(BASE_DIR, '..', 'venv', 'lib', 
                                PYTHON_VERSION, 'site-packages'))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
