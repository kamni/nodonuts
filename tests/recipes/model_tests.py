from django.db import transaction, IntegrityError
from django.test import TestCase
from django_test_utils.model_utils import TestUser

from recipes.models import *


class RecipeTests(TestCase):
    def test__init(self):
        user = TestUser()
        
        # all fields except date_added
        recipe = Recipe.objects.create(title="Fresh Peaches",
                                       slug="fresh-peaches-ftw",
                                       short_description="Delicious!",
                                       image="nothing.jpg",
                                       thumbnail="nothing-thumb.jpg",
                                       ingredients="2 peaches",
                                       instructions="Eat peaches, sans pits",
                                       featured=True,
                                       is_public=True,
                                       added_by=user)
        self.assertIsNotNone(recipe.date_added)
        
        # bare minimum fields
        recipe = Recipe.objects.create(title="Fresh Strawberries",
                                       short_description="Mmmm",
                                       ingredients="1 cup strawberries",
                                       instructions="Pop in mouth. Enjoy!",
                                       added_by=user)
        self.assertEquals("fresh-strawberries", recipe.slug)
        self.assertFalse(recipe.featured)
        self.assertTrue(recipe.is_public)
        self.assertIsNotNone(recipe.date_added)
        
        # title must be unique
        with transaction.atomic():
            self.assertRaises(IntegrityError, Recipe.objects.create,
                              title="Fresh Peaches", short_description="Hooray!",
                              ingredients="3 peaches", instructions="Eat them",
                              added_by=user)
        
        # slug must be unique
        with transaction.atomic():
            self.assertRaises(IntegrityError, Recipe.objects.create,
                              title="Celery and Carrots", slug="fresh-strawberries",
                              short_description="Crunch", 
                              ingredients="Celery and Carrots",
                              instructions="Cut into sticks and eat one at a time",
                              added_by=user)
        
        # title required
        with transaction.atomic():
            self.assertRaises(IntegrityError, Recipe.objects.create,
                              short_description="Nothing", ingredients="Nothing",
                              instructions="Do Nothing", added_by=user)
        
        # short_description required
        with transaction.atomic():
            self.assertRaises(IntegrityError, Recipe.objects.create,
                              title="Watermelon", ingredients="1 Watermelon",
                              instructions="Cut into slices and eat",
                              added_by=user)
        
        # ingredients required
        with transaction.atomic():
            self.assertRaises(IntegrityError, Recipe.objects.create,
                              title="Blueberries", short_description="Very blue",
                              instructions="Wash, serve with cream", added_by=user)
        
        # instructions required
        with transaction.atomic():
            self.assertRaises(IntegrityError, Recipe.objects.create,
                              title="Sliced Apples",
                              short_description="Crunchy and Tangy",
                              ingredients="2 granny smith apples", added_by=user)
        
        # added_by required
        with transaction.atomic():
            self.assertRaises(IntegrityError, Recipe.objects.create,
                              title="An Orange", short_description="Juicy",
                              ingredients="1 orange", instructions="Peel and eat")
    
    def test__repr(self):
        pass
    
    def test__unicode(self):
        pass