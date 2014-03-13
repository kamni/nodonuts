import re

from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.utils import timezone
from django_enumfield import enum
from null_reality.models import NullCheckerModel
from null_reality.fields import NullableCharField, NullableTextField

from recipes.utils import wilson_score_interval


class ServingSize(enum.Enum):
    """Tracks how many people should be able to have a full serving of a Recipe"""
    ONE_TO_TWO = 0
    THREE_TO_FOUR = 1
    FIVE_TO_SIX = 2
    SEVEN_TO_NINE = 3
    TEN_TO_TWELVE = 4
    TWELVE_TO_FIFTEEN = 5
    FIFTEEN_TO_TWENTY = 6
    TWENTY_TO_THIRTY = 7
    THIRTY_TO_FIFTY = 8
    MORE = 9

    @classmethod
    def labels(cls):
        return {0: "1-2 people",
                1: "3-4 people",
                2: "5-6 people",
                3: "7-9 people",
                4: "10-12 people",
                5: "12-15 people",
                6: "15-20 people",
                7: "20-30 people",
                8: "30-50 people",
                9: "A small army"}


class RecipeManager(models.Manager):
    """
    Custom model manager for the Recipe class.
    
    Provides the following additional methods:
    
        filter_featured
        filter_newest
    """
    def filter_featured(self, limit=None):
        """
        Finds Recipes where the 'featured' flag is set to true.
        If the limit parameter is specified, only returns that many results. If
        limit is None, returns all Recipes.
        
        :param limit: positive integer indicating the number of results to return
        :return: queryset of Recipes
        """
        query = self.filter(featured=True, is_public=True).order_by('-date_added')
        if limit:
            query = query[:limit]
        return query
    
    def filter_newest(self, limit=None):
        """
        Finds and returns recipes, ordered with the newest recipes first.
        If the limit parameter is specified, only returns that many results. If
        limit is None, returns all Recipes.
        
        :param limit: positive integer indicating the number of results to return
        :return: queryset of Recipes
        """
        query = self.filter(is_public=True).order_by('-date_added')
        if limit:
            query = query[:limit]
        return query


class Recipe(NullCheckerModel):
    """
    Stores recipes that users can find on the site.
    
    :field title: CharField, max_length=80, unique=True
    :field slug: SlugField, unique=True, defaults to slugified version of title
    :field short_description: CharField, max_length=200
    :field image: ImageField, uploads to 'recipes/images', optional
    :field thumbnail: ImageField, uploads to 'recipes/thumbs', optional
    :field ingredients: TextField
    :field instructions: TextField
    :field featured: BooleanField, defaults to False
    :field is_public: BooleanField, defaults to True
    :field added_by: ForeignKey to User
    :field date_added: DateTimeField, defaults to timezone.now
    """
    title = NullableCharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True, blank=True, 
                            help_text="URL slug that will be used for this " +
                            "recipe's address. This will be generated automatically.")
    short_description = NullableCharField(max_length=200)
    serving_size = enum.EnumField(ServingSize, default=2, 
                                  help_text="Number of people this recipe " +
                                  "serves")
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
    date_added = models.DateTimeField(default=timezone.now)
    popularity = models.DecimalField(max_digits=10, decimal_places=4, default=0,
                                     help_text="Calculated score based on the " +
                                     "number of ratings")
    likes = models.PositiveIntegerField(default=0, help_text="Denormalized count " +
                                        "of the number of people who liked this " +
                                        "recipe.")
    dislikes = models.PositiveIntegerField(default=0, help_text="Denormalized count " +
                                          "of the number of people who disliked this " +
                                          "recipe.")
    
    objects = RecipeManager()
    
    class Meta:
        ordering = ('-popularity', 'title')
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.ingredients = re.sub("<p>", "", re.sub("</p>", "<br />", self.ingredients))
        super(Recipe, self).save(*args, **kwargs)
    
    def serving_size_label(self):
        """TODO: docs and tests"""
        return ServingSize.label(self.serving_size)
    
    def summary_id(self):
        """TODO: docs and tests"""
        return "-".join(("summary", self.slug))
    
    def __repr__(self):
        return "<Recipe: %s (by %s)>" % (self.title, self.added_by)
    
    def __unicode__(self):
        return unicode(self.title)


class TagType(enum.Enum):
    """
    Classifications for RecipeTags. 
    
    Types:
        MISCELLANEOUS: default tag, an easy way to identify new tags 
                created by users
        MEALS: a particular kind of eating situation (breakfast, lunch, finger
            food)
        INGREDIENTS: a classification based on the types of ingredients in a
            recipe (vegan, low-carb, gluten-free)
            passover/pesach, finger food)
    """
    INGREDIENTS = 1
    MEALS = 2
    MISCELLANEOUS = 100


class RecipeTagManager(models.Manager):
    """
    TODO: docs and tests
    """
    def filter_list(self, exclude_miscellaneous=False):
        # TODO: docs and tests
        tags = RecipeTag.objects.exclude(recipe__isnull=True)
        if exclude_miscellaneous:
            tags = tags.exclude(type=TagType.MISCELLANEOUS)
        return tags


class RecipeTag(NullCheckerModel):
    """
    A way for users to classify recipes.
    
    :field name: CharField, max length=30, unique
    :field type: EnumField using TagType
    :field is_public: BooleanField, defaults to True
    :field added_by: ForeignKey to User, nullable
    :field date_added: DateTimeField, defaults to timezone.now
    """
    name = NullableCharField(max_length=15, unique=True)
    type = enum.EnumField(TagType, default=TagType.MISCELLANEOUS)
    is_public = models.BooleanField(default=True, help_text="Indicates whether " +
                                    "all users will see this tag")
    added_by = models.ForeignKey(User, blank=True, null=True,
                                 help_text="The user who added this tag")
    date_added = models.DateTimeField(default=timezone.now)
    
    objects = RecipeTagManager()
    
    class Meta:
        ordering = ('type', 'name')
    
    def clean(self):
        other_tag = RecipeTag.objects.filter(name=self.name.lower()).exclude(id=self.id)
        if other_tag:
            raise ValidationError("This tag already exists")
        return super(RecipeTag, self).clean()
    
    def get_type_label(self):
        # TODO: docs, tests
        return TagType.label(self.type)
    
    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.lower()
        super(RecipeTag, self).save(*args, **kwargs)
    
    def who_added(self):
        """ Returns a display-friendly version of the user that added the tag """
        return self.added_by.get_full_name() if self.added_by else "System"
    
    def __repr__(self):
        return "<RecipeTag: %s>" % self.name
    
    def __unicode__(self):
        return unicode(self.name)


class Rating(models.Model):
    """
    A way for users to give a 'like' or a 'dislike' to recipes. Users may only
    have one rating per recipe.
    
    :field recipe: ForeignKey to Recipe
    :field rated_by: ForeignKey to User
    :field vote: SmallIntegerField, can only take values of 1 or -1
    :field last_updated: DateTimeField, auto_now
    """
    recipe = models.ForeignKey('Recipe')
    rated_by = models.ForeignKey(User)
    vote = models.BooleanField("Whether the user up-voted or down-voted this " +
                               "recipe. 'False' represents a 'dislike' and " +
                               "'True' represents a 'like'")
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('recipe', 'rated_by')
    
    def liked_text(self):
        """Returns the text for displaying the rating for this user"""
        return ["disliked", "liked"][int(self.vote > 0)]
    
    def save(self, *args, **kwargs):
        super(Rating, self).save(*args, **kwargs)
        self.set_recipe_popularity()
        
    def set_recipe_popularity(self):
        """ Updates the popularity on self.recipe based on the newest vote """
        ratings = Rating.objects.filter(recipe=self.recipe)
        ups = ratings.filter(vote=True).count()
        downs = ratings.filter(vote=False).count()
        self.recipe.popularity = str(wilson_score_interval(ups, downs))
        self.recipe.likes = ups
        self.recipe.dislikes = downs
        self.recipe.save()
    
    def __repr__(self):
        return "<Rating: %s (%s)>" % (self.recipe, self.rated_by)
    
    def __unicode__(self):
        return unicode(self.liked_text())
