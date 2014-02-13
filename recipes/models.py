from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django_enumfield import enum

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
    tags = models.ManyToManyField('RecipeTag', blank=True, null=True)
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


class TagType(enum.Enum):
    """
    Classifications for RecipeTags. 
    
    Types:
        OTHER: default tag, an easy way to identify new tags created by users
        MEAL: a particular kind of eating situation (breakfast, lunch, finger
            food)
        INGREDIENT: a classification based on the types of ingredients in a
            recipe (vegan, low-carb, gluten-free)
            passover/pesach, finger food)
    """
    OTHER = 0
    INGREDIENT = 1
    MEAL = 2


class RecipeTag(NullCheckerModel):
    """
    A way for users to classify recipes.
    
    :field tag: CharField, max length=30, unique
    :field type: EnumField using TagType
    :field is_public: BooleanField, defaults to True
    :field added_by: ForeignKey to User, nullable
    :field date_added: DateTimeField, auto_now_add
    """
    tag = NullableCharField(max_length=30, unique=True)
    type = enum.EnumField(TagType, default=TagType.OTHER)
    is_public = models.BooleanField(default=True)
    added_by = models.ForeignKey(User, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('type', 'tag')
    
    def save(self, *args, **kwargs):
        if self.tag:
            self.tag = self.tag.lower()
        super(RecipeTag, self).save(*args, **kwargs)
    
    def who_added(self):
        """ Returns a display-friendly version of the user that added the tag """
        return self.added_by.get_full_name() if self.added_by else "System"
    
    def __repr__(self):
        return "<RecipeTag: %s>" % self.tag
    
    def __unicode__(self):
        return unicode(self.tag)
