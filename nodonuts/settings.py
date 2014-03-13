"""
Django settings for community_plate project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import datetime
import os

from django.conf import global_settings


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+*smmhy!zvhsosmy^vah6mvi$j7nquwpg^2!m!h-*mq3@w1ye@'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'constance.context_processors.config',
)


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # third-party
    'constance.backends.database',
    'constance',
    'django_nose',
    'djcelery',
    'haystack',
    'kombu.transport.django',
    'social.apps.django_app.default',
    'sphinxdoc',
    'tinymce',
    
    # this project
    'organizations',
    'recipes',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'nodonuts.urls'

WSGI_APPLICATION = 'nodonuts.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static asset configuration
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_ROOT = 'uploads'
MEDIA_URL = '/media/'


# haystack (search) setting
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}

# celery settings, configured for db queue. Please update in srv_settings.py
BROKER_URL = 'django://'
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERYBEAT_SCHEDULE = {
    'update-recipe-search-index': {
        'task': 'recipes.tasks.update_recipe_indexes',
        'schedule': datetime.timedelta(hours=1),
    },
}
CELERY_TIMEZONE = TIME_ZONE


# Sphinx config
SPHINXDOC_BUILD_DIR = 'build'
INCLUDE_DOC_URLS = True
DISPLAY_DOC_LINKS = True


# Nose configuration
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['-s', '--logging-level=CRITICAL']


# Production server settings that we don't want to keep in the repository
try:
    from srv_settings import *
except ImportError:
    pass


# constance settings
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    'SITE_NAME': ('NoDonuts', 'The name to display in headers, title bar, ' +
                  'and copyright notices'),
    'SITE_LOGO': ('img/logo.png', 'The path to the file located in the static folder ' +
                  'that represents the logo. Leave off any starting slash (/)'),
    'SHOW_SITE_LOGO': (True, 'Logo, if configured, should be shown in the ' +
                       'header area of pages'),
    'COPYRIGHT': ('Copyright', 'The type of intellectual property rights ' +
                  'that content on this site has. Suggestions: Copyleft, ' +
                  'Creative Commons Attribution Share-Alike'),
    'COPYRIGHT_MESSAGE': ('', 'An additional message for your copyright. ' +
                          'Example: All rights reserved.'),
    'FEATURED_RECIPE_COUNT': (8, 'How many featured recipes should be shown ' +
                                   'on the home page.'),
    'NEWEST_RECIPE_COUNT': (8, 'How many of the newest recipes should be ' +
                               'shown on the home page.'),
    'SEARCH_RESULTS_PER_PAGE': (10, 'Number of search results to show on ' +
                                    'search page.'),
    'DISPLAY_DOC_LINKS': (INCLUDE_DOC_URLS and DISPLAY_DOC_LINKS, 'Show links ' +
                          'to the project documentation in the nav bar'),
    'SUPERUSER_DOCS_ONLY': (True, 'If documentation links are available, only ' +
                            'show docs to superusers.'),
    'DISPLAY_TERMS_AND_CONDITIONS': (True, 'Whether to make the terms and ' +
                                     'conditions page available to users.'),
    'DISPLAY_PRIVACY_POLICY': (True, 'Make the privacy policy available to users'),
}  
