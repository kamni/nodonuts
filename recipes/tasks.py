import datetime
import logging

from celery.decorators import periodic_task
from django.core.management import call_command

from nodonuts import celery_app


@celery_app.task
def update_recipe_indexes():
    """TODO: docs"""
    call_command('update_index recipes')