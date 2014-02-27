"""
Django settings for community_plate project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from django.conf import global_settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
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
    'haystack',
    'tinymce',
    'social.apps.django_app.default', 
    
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
}


# haystack (search) setting
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}


# Nose configuration
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['-s', '--logging-level=CRITICAL']


# Developer settings that won't be available on the live site
try:
    from dev_settings import *
except ImportError:
    pass

# Production server settings that we don't want to keep in the repository
try:
    from srv_settings import *
except ImportError:
    pass


    
