from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Recipe(models.Model):
    """
    Stores recipes that users can find on the site.
    """
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True, blank=True, help_text="URL slug that " +
                            "will be used for this recipe's address. If you " +
                            "leave this field blank, it will default to a " +
                            "slugified version of the title.")
    short_description = models.CharField(max_length=200)
    image = models.ImageField(upload_to=settings.RECIPE_IMAGE_FOLDER,
                              help_text="Display image for the recipe. The " +
                              "ideal image size is 200x200px.")
    thumbnail = models.ImageField(upload_to=settings.RECIPE_THUMBNAIL_FOLDER,
                                  help_text="Smaller image to use for the " +
                                  "recipe. Ideal image size is 60x60px")
    ingredients = models.TextField(help_text="Ingredients (with measurements)" +
                                   "for the recipe, one ingredient per line.")
    instructions = models.TextField(help_text="Instructions for preparing the " +
                                    "recipe.")
    featured = models.BooleanField(default=False, help_text="If true, this " +
                                   "recipe will show up under the 'Featured' " +
                                   "section of the home page")
    is_public = models.BooleanField(default=True, help_text="If false, this " +
                                    "recipe will not show up in public searches")
    added_by = models.ForeignKey(User, help_text="User who created this recipe.")
    date_added = models.DateTimeField(auto_add_now=True)
    
    def __repr__(self):
        return "<Recipe: %s (by %s)>" % (self.title, self.added_by)
    
    def __unicode__(self):
        return unicode(self.title)
