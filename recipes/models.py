from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

from null_reality.models import NullCheckerModel
from null_reality.fields import NullableCharField, NullableTextField


class Recipe(NullCheckerModel):
    """
    Stores recipes that users can find on the site.
    
    :field title: CharField, max_length=150, unique=True
    :field slug: SlugField, unique=True, defaults to slugified version of title
    :field short_description: CharField, max_length=200
    :field image: ImageField, uploads to 'recipes/images', optional
    :field thumbnail: ImageField, uploads to 'recipes/thumbs', optional
    :field ingredients: TextField
    :field instructions: TextField
    :field featured: BooleanField, defaults to False
    :field is_public: BooleanField, defaults to True
    :field added_by: ForeignKey to User
    :field date_added: DateTimeField, auto_now_add
    """
    title = NullableCharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True, blank=True, help_text="URL slug that " +
                            "will be used for this recipe's address. If you " +
                            "leave this field blank, it will default to a " +
                            "slugified version of the title.")
    short_description = NullableCharField(max_length=200)
    image = models.ImageField(upload_to='recipes/images', blank=True, null=True,
                              help_text="Display image for the recipe. The " +
                              "ideal image size is 200x200px.")
    thumbnail = models.ImageField(upload_to='recipes/thumbs', blank=True, null=True,
                                  help_text="Smaller image to use for the " +
                                  "recipe. Ideal image size is 60x60px")
    ingredients = NullableTextField(help_text="Ingredients (with measurements) " +
                                   "for the recipe, one ingredient per line.")
    instructions = NullableTextField(help_text="Instructions for preparing the " +
                                    "recipe.")
    featured = models.BooleanField(default=False, help_text="If true, this " +
                                   "recipe will show up under the 'Featured' " +
                                   "section of the home page")
    is_public = models.BooleanField(default=True, help_text="If false, this " +
                                    "recipe will not show up in public searches")
    added_by = models.ForeignKey(User, help_text="User who created this recipe.")
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('title', 'id')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Recipe, self).save(*args, **kwargs)
    
    def __repr__(self):
        return "<Recipe: %s (by %s)>" % (self.title, self.added_by)
    
    def __unicode__(self):
        return unicode(self.title)
