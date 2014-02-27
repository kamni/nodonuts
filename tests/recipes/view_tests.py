import random

from django.test import TestCase

from recipes.models import Recipe, RecipeTag
from recipes.views import *
from tests.model_tests import TestRecipe, TestRecipeTag


class HomeTests(TestCase):
    def test_get_context_data(self):
        Recipe.objects.all().delete()
        RecipeTag.objects.all().delete()
        view = Home()
        
        # expected context when there is no recipe content in the database
        context = view.get_context_data()
        self.assertEqual(3, len(context))
        self.assertEqual([], list(context.get('featured_recipes')))
        self.assertEqual([], list(context.get('newest_recipes')))
        self.assertEqual([], list(context.get('tags')))
        
        # newest recipes
        newest_recipes = [TestRecipe() for i in range(9)]
        expected_newest = newest_recipes[1:]
        expected_newest.reverse()
        context = view.get_context_data()
        self.assertEqual([], list(context.get('featured_recipes')))
        self.assertEqual(expected_newest, list(context.get('newest_recipes')))
        self.assertEqual([], list(context.get('tags')))
        
        # tags and newest recipes
        self.assertTrue(False, "Not Complete")
        
        
        # tags, newest recipes and featured recipes