from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.test import TestCase
from django_test_utils.model_utils import TestUser
from django_test_utils.random_generators import lorem_ipsum

from recipes.models import *
from recipes.utils import wilson_score_interval


class RecipeTests(TestCase):
    def test_save(self):
        user = TestUser()
        
        # should create slug if it isn't set
        recipe = Recipe.objects.create(title="Apple Cider",
                                       short_description="A tasty fall drink",
                                       ingredients="1 barrel of apples",
                                       instructions="Get creative",
                                       added_by=user)
        self.assertEqual('apple-cider', recipe.slug)
        
        # should change the slug to match the title
        recipe.title = "Apple Juice"
        recipe.save()
        recipe = Recipe.objects.get(id=recipe.id)
        self.assertEqual('apple-juice', recipe.slug)
    
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
        self.assertEqual("fresh-strawberries", recipe.slug)
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
                              title="Fresh-Strawberries", slug="fresh-strawberries",
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
        recipe = Recipe(title="PB&J", added_by=user)
        self.assertEqual("<Recipe: PB&J (by %s)>" % user, repr(recipe))
    
    def test__unicode(self):
        recipe = Recipe(title="Club Soda")
        self.assertEqual(u"Club Soda", unicode(recipe))
    
    
class RecipeTagTests(TestCase):
    def test_clean(self):
        rt1 = TestRecipeTag(name="amazing")
        
        # should catch duplicates, case-insensitive
        rt2 = RecipeTag(name="amazing")
        self.assertRaises(ValidationError, rt2.clean)
        rt3 = RecipeTag(name="AmAzInG")
        self.assertRaises(ValidationError, rt3.clean)
        
        # should not catch self
        rt1.clean()
    
    def test_save(self):
        # should lower-case the name
        rt = RecipeTag(name="MMMMM")
        rt.save()
        self.assertEqual("mmmmm", rt.name)
    
    def test__init(self):
        # all fields
        rt = RecipeTag.objects.create(name="Testing1",
                                      type=TagType.MEAL,
                                      is_public=False,
                                      added_by=TestUser())
        self.assertIsNotNone(rt.date_added)
        self.assertEqual('testing1', rt.name)
        
        # bare minimum fields
        rt = TestRecipeTag(name="Testing2")
        self.assertEqual('testing2', rt.name)
        self.assertEqual(TagType.OTHER, rt.type)
        self.assertTrue(rt.is_public)
        self.assertIsNone(rt.added_by)
        self.assertIsNotNone(rt.date_added)
        
        # name must be unique, case-insensitive
        with transaction.atomic():
            self.assertRaises(IntegrityError, RecipeTag.objects.create,
                              name="testing1")
        
        # name is required
        with transaction.atomic():
            self.assertRaises(IntegrityError, RecipeTag.objects.create)
        
    def test__repr(self):
        rt = RecipeTag(name="yummy1")
        self.assertEqual("<RecipeTag: yummy1>", repr(rt))
    
    def test__unicode(self):
        rt = RecipeTag(name="yummy2")
        self.assertEqual(u'yummy2', unicode(rt))
        

class RatingTests(TestCase):
    def test__init(self):
        rated_by = TestUser()
        
        # all fields
        rcpe1 = TestRecipe()
        r1 = Rating.objects.create(recipe=rcpe1,
                                   rated_by=rated_by,
                                   vote=1)
        self.assertIsNotNone(r1.last_updated)
        
        # recipe and rated_by should be unique
        with transaction.atomic():
            self.assertRaises(IntegrityError, Rating.objects.create,
                              recipe=rcpe1, rated_by=rated_by, vote=1)
        self.assert_(Rating.objects.create(recipe=rcpe1, rated_by=TestUser(),
                                           vote=1))
        self.assert_(Rating.objects.create(recipe=TestRecipe(), rated_by=rated_by,
                                           vote=-1))
        
        # recipe is required
        with transaction.atomic():
            self.assertRaises(IntegrityError, Rating.objects.create,
                              rated_by=rated_by, vote=-1)
        
        # rated_by is required
        with transaction.atomic():
            self.assertRaises(IntegrityError, Rating.objects.create,
                              recipe=rcpe1, vote=1)
        
        # vote is required
        with transaction.atomic():
            self.assertRaises(IntegrityError, Rating.objects.create,
                              recipe=TestRecipe(), rated_by=TestUser())
    
    def test_liked_text(self):
        r1 = Rating(vote=1)
        self.assertEqual("liked", r1.liked_text())
        
        r2 = Rating(vote=-1)
        self.assertEqual("disliked", r2.liked_text())
    
    def test_save(self):
        recipe = TestRecipe()
        self.assertEqual(0, recipe.popularity)
        
        for i in range(1, 5):
            TestRating(recipe=recipe, vote=True)
            recipe = Recipe.objects.get(id=recipe.id)
            wsi = wilson_score_interval(i, 0)
            self.assertEqual(Decimal(wsi).quantize(Decimal('.0001')), 
                             recipe.popularity)
        
        for i in range(1, 5):
            TestRating(recipe=recipe, vote=False)
            recipe = Recipe.objects.get(id=recipe.id)
            wsi = wilson_score_interval(4, i)
            self.assertEqual(Decimal(wsi).quantize(Decimal('.0001')), 
                             recipe.popularity)
    
    def test_set_recipe_popularity(self):
        recipe = TestRecipe()
        for i in range(3):
            TestRating(recipe=recipe, vote=True)
        expected_rating = Decimal(wilson_score_interval(3, 0)).quantize(Decimal('.0001'))
        recipe = Recipe.objects.get(id=recipe.id)
        self.assertEqual(expected_rating, recipe.popularity)
        
        # only sets popularity for ratings stored in the db
        rating = Rating(recipe=recipe, rated_by=TestUser(), vote=False)
        rating.set_recipe_popularity()
        recipe = Recipe.objects.get(id=recipe.id)
        self.assertEqual(expected_rating, recipe.popularity)
        
        # default case, and no error/change when calling twice on same 
        # unchanged rating
        rating.save()
        rating.set_recipe_popularity()
        new_rating = Decimal(wilson_score_interval(3, 1)).quantize(Decimal('.0001'))
        recipe = Recipe.objects.get(id=recipe.id)
        self.assertNotEqual(expected_rating, new_rating)
        self.assertEqual(new_rating, recipe.popularity)
        rating.set_recipe_popularity()
        recipe = Recipe.objects.get(id=recipe.id)
        self.assertEqual(new_rating, recipe.popularity)
    
    def test__repr(self):
        rcpe = TestRecipe()
        user = TestUser()
        r1 = Rating(recipe=rcpe, rated_by=user)
        self.assertEqual("<Rating: %s (%s)>" % (rcpe, user), repr(r1))
    
    def test__unicode(self):
        r1 = Rating(vote=1)
        self.assertEqual(u'liked', unicode(r1))
        
        r2 = Rating(vote=-1)
        self.assertEqual(u'disliked', unicode(r2))


############# Test Models ################

def TestRecipe(title=None, slug=None, short_description=None, image=None,
               thumbnail=None, ingredients=None, instructions=None, 
               featured=False, is_public=True, added_by=None, popularity=None):
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


def TestRecipeTag(name=None, type=TagType.OTHER, is_public=True, added_by=None):
    # generating unique name
    if not name:
        name_base = lorem_ipsum(1)
        suffix = 1
        not_unique = True
        while not_unique:
            name = "%s%s" % (name_base, suffix)
            not_unique = RecipeTag.objects.filter(name=name)
            suffix += 1
            
    return RecipeTag.objects.create(name=name,
                                    type=type,
                                    is_public=is_public,
                                    added_by=added_by)


def TestRating(recipe=None, rated_by=None, vote=True):
    return Rating.objects.create(recipe=recipe or TestRecipe(),
                                 rated_by=rated_by or TestUser(),
                                 vote=vote)
    