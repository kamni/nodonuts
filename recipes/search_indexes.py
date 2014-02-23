import datetime
from haystack import indexes
from recipes.models import Recipe


class RecipeIndex(indexes.SearchIndex, indexes.Indexable):
    recipe_text = indexes.CharField(document=True, use_template=True)
    added_by = indexes
    #.CharField(model_attr='added_by')
    popularity = indexes.DateTimeField(model_attr='popularity')
    #is_public = indexes.
    
    # filter by added_by, is_public
    # search by text in title, ingredients
    # search by tag
    # filter by popularity

    def get_model(self):
        return Recipe

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(date_added__lte=datetime.datetime.now())