from django.db import transaction, IntegrityError
from django.test import TestCase
from django_test_utils.model_utils import TestUser
from django_test_utils.random_generators import lorem_ipsum

from recipes.models import *


class RecipeTests(TestCase):
    def test_save(self):
        user = TestUser()
        
        # should create slug if it isn't set
        recipe = Recipe.objects.create(title="Apple Cider",
                                       short_description="A tasty fall drink",
                                       ingredients="1 barrel of apples",
                                       instructions="Get creative",
                                       added_by=user)
        self.assertEquals('apple-cider', recipe.slug)
        
        # should not change slug if it exists
        recipe.title = "Apple Juice"
        recipe.save()
        recipe = Recipe.objects.get(id=recipe.id)
        self.assertEquals('apple-cider', recipe.slug)
    
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
        user = TestUser()
        recipe = TestRecipe(title="PB&J", added_by=user)
        self.assertEquals("<Recipe: PB&J (by %s)>" % user, repr(recipe))
    
    def test__unicode(self):
        recipe = TestRecipe(title="Club Soda")
        self.assertEquals(u"Club Soda", unicode(recipe))
    

def TestRecipe(title=None, slug=None, short_description=None, image=None,
               thumbnail=None, ingredients=None, instructions=None, 
               featured=False, is_public=True, added_by=None):
    # generating a unique title
    if not title:
        title_base = lorem_ipsum(3)
        suffix = 1
        not_unique = True
        while not_unique:
            title = "%s %s" % (title_base, suffix)
            not_unique = Recipe.objects.filter(title=title)
            suffix += 1
        
    return Recipe.objects.create(title=title,
                                 slug=slug,
                                 short_description=short_description or lorem_ipsum(3),
                                 image=image,
                                 thumbnail=thumbnail,
                                 ingredients=ingredients or lorem_ipsum(7),
                                 instructions=instructions or lorem_ipsum(7),
                                 featured=featured,
                                 is_public=is_public,
                                 added_by=added_by or TestUser())
    
    
    
    
    is_public = models.BooleanField(default=True, help_text="If false, this " +
                                    "recipe will not show up in public searches")
    added_by = models.ForeignKey(User, help_text="User who created this recipe.")
    date_added = models.DateTimeField(auto_now_add=True)