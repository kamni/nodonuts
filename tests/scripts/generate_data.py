"""
Simple script to generate some test data for development
"""
import os
import random
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)).rsplit(os.sep, 2)[0])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nodonuts.settings")

from django.core.management import call_command
from django_test_utils.model_utils import TestUser
from django_test_utils.random_generators import lorem_ipsum

from recipes.models import Recipe, RecipeTag, Rating
from tests.recipes.model_tests import TestRecipe, TestRecipeTag, TestRating


QUANTITIES = ['1', '1/2', '1/4', '1/8', '2', '2 1/2', '3', '3 1/2', '8', '16']

UNITS = ['cup', 'tsp', 'tbsp']

WEIGHTS = ['oz', 'lb']

MEASURED_INGREDIENTS = ['flour', 'sugar', 'salt', 'baking soda', 'butter',
                        'vinegar', 'nutmeg', 'cinnamon', 'cloves', 'dill',
                        'baking powder', 'vanilla extract', 'thyme', 'parsley',
                        'rice', 'cooked pasta', 'tomato paste', 'shredded cheese',
                        'walnuts', 'cranberries', 'water chestnuts', 'curry powder',
                        'peeled grapes', 'lard', 'sour cream', 'garlic']

SINGLE_INGREDIENTS = ['large onion', 'mushroom', 'green onion', 
                      'rosemary sprig', 'orange', 'lemon', 'banana', 'apple',
                      'watermelon', 'plantain', 'cabbage', 'turnip', 'carrot',
                      'bread slice', 'green pepper', 'red pepper', 'peach']

WEIGHED_INGREDIENTS = ['potatoes', 'beef', 'pork', 'tofu', 'shrimp', 
                       'strawberries', 'blueberries', 'crab', 'chicken',
                       'frozen vegetable medley']

LIQUID_INGREDIENTS = ['sherry', 'milk', 'water', 'beer']

NAMES = ["Betty's", "Tom's", "Frank's", "Ella's", "Mark's", "Amy's", 
         "Constance's", "Patricia's", "Ellen's", "Eric's", "Sam's", "David's"]

ADJECTIVES = ['Amazing', 'Awesome', 'Delicious', 'Quick', 'Easy', 'Tasty',
             'Effortless', 'Savory', 'Sweet']

DAYS_OF_THE_WEEK = ['Sunday', 'Wednesday', 'Friday', 'Midweek', 'Weekend',
                    'Everyday', 'Morning', 'Tea Time']

COOKING_METHOD = ['Crockpot', 'Dutch Oven', 'Fried', 'Sauteed', 'Seasoned',
                  'Barbequed', 'Frozen', 'Baked', 'Roasted', 'Stuffed']

DISH = ['Crepes', 'Casserole', 'Stew', 'Remoulade', 'Sandwich', 'Turnovers',
        'Pie', 'Risotto', 'Pasta', 'Flambe', 'Portifino', 'Bake']

OPENING_INSTRUCTIONS = ["Preheat oven to 450 degrees.", "Preheat the oven to " +
                        "325 degrees.", "Chop all fruits and vegetables into " +
                        "cubes.", "Blend ingredients in a food processor " +
                        "coarsely.", "Puree all ingredients finely."]

SECOND_INSTRUCTIONS = ["Mix all ingredients quickly, adding liquid as needed.", 
                       "Pan fry meat until lightly browned.",
                       "Add liquid slowly, stiring until mixture has a " +
                       "single consistency.", "Strain through a cheese cloth, " +
                       "retaining the liquid for later use."]

MIDDLE_INSTRUCTIONS = ["Bake in the oven for 20 minutes.", "Bake in the oven " +
                       "until golden brown.", "Boil on low for 8-10 minutes.",
                       "Set in refrigerator for 30 minutes until firm.", 
                       "Sautee until crispy.", "Cook in a sauce " +
                       "pan on high, stirring vigorously."]

ENDING_INSTRUCTIONS = ["Garnish with parsley, if desired.", "Serve and enjoy!",
                       "Bon appetite!", "Scoop into bowls and serve.",
                       "Salt and pepper to taste.", "Slice into equal portions " +
                       "and serve."]


def generate_test_data():
    def make_ingredient(category):
        ingredient = random.choice(category)
        
        if category in (MEASURED_INGREDIENTS, LIQUID_INGREDIENTS):
            units = random.choice(UNITS)
        elif category == WEIGHED_INGREDIENTS:
            units = random.choice(WEIGHTS)
        else:
            units = None
        
        quantity = random.choice(QUANTITIES)
        if quantity not in ('1', '1/2', '1/4', '1/8'):
            if units:
                if units in ('cup', 'lb'):
                    units += "s"
            else:
                ingredient += "s"
        
        if units:
            return " ".join([quantity, units, ingredient])
        return " ".join([quantity, ingredient])
    
    def make_ingredients_list():
        ingredients = []
        for i in range(random.randint(2, 4)):
            ingredients.append(make_ingredient(MEASURED_INGREDIENTS))
        for i in range(random.randint(1, 2)):
            ingredients.append(make_ingredient(SINGLE_INGREDIENTS))
        for i in range(random.randint(1, 2)):
            ingredients.append(make_ingredient(WEIGHED_INGREDIENTS))
        for i in range(random.randint(0, 1)):
            ingredients.append(make_ingredient(LIQUID_INGREDIENTS))
        
        random.shuffle(ingredients)
        return "<br>".join(ingredients) 
    
    def make_title():
        words = []
        for word_group in (NAMES, ADJECTIVES, DAYS_OF_THE_WEEK, COOKING_METHOD,
                           SINGLE_INGREDIENTS, DISH):
            use = random.randint(0, 1)
            if use or word_group in (SINGLE_INGREDIENTS, DISH):
                title_word = random.choice(word_group)
                
                # we have to pull this one out individually because title-
                # casing words like "Amy's" does strange things with the
                # capitalization
                if word_group == SINGLE_INGREDIENTS:
                    title_word = title_word.title()
                words.append(title_word)

        return " ".join(words)
    
    def make_instructions():
        instructions = []
        for inst in (OPENING_INSTRUCTIONS, SECOND_INSTRUCTIONS, 
                     MIDDLE_INSTRUCTIONS, ENDING_INSTRUCTIONS):
            number_to_choose = random.randint(1, 2)
            for i in range(number_to_choose):
                instructions.append(random.choice(inst))
        
        return " ".join(instructions)

    print "Making users..."
    users = [TestUser() for i in range(30)]\
    
    print "Creating tags..."
    call_command('loaddata', 'recipe_tags')
    for i in range(10):
        TestRecipeTag(is_public=bool(random.randint(0, 1)),
                      added_by=random.choice(users))
    
    print "Adding recipes and ratings..."
    for i in range(250):        
        title = make_title()
        while Recipe.objects.filter(title=title):
            title = make_title()
        
        featured = random.randint(1, 20) == 1
        is_public = random.randint(1, 30) != 1
        recipe = TestRecipe(title=title, 
                            short_description=lorem_ipsum(random.randint(5, 8)),
                            ingredients=make_ingredients_list(),
                            instructions=make_instructions(), 
                            featured=featured, is_public=is_public,
                            added_by=random.choice(users))
        
        selected_tags = []
        num_tags = random.randint(1, 4)
        tags = RecipeTag.objects.all()
        while len(selected_tags) < num_tags:
            tag = random.choice(tags)
            if tag not in selected_tags:
                selected_tags.append(tag)
        for tag in selected_tags:
            recipe.tags.add(tag)
        
        rated_users = []
        num_ratings = random.randint(0, 20)
        while len(rated_users) < num_ratings:
            rated_by = random.choice(users)
            if rated_by not in rated_users:
                rated_users.append(rated_by)
        for user in rated_users:
            vote = random.randint(1, 10) != 10
            TestRating(recipe=recipe, rated_by=user, vote=vote)
    
    print "30 users and 250 recipes created. Done!"


if __name__ == '__main__':
    generate_test_data()