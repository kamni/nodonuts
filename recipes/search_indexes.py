import datetime

from django.utils import timezone
from haystack import indexes

from recipes.models import Recipe


class RecipeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    tags = indexes.MultiValueField()
    date_added = indexes.DateTimeField(model_attr='date_added')
    popularity = indexes.DecimalField(model_attr='popularity')
    title = indexes.CharField(model_attr="title")
    
    # TODO: filter by added_by, is_public -- do in a custom search class

    def get_model(self):
        return Recipe

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(date_added__lte=timezone.now())
    
    def prepare(self, object):
        self.prepared_data = super(RecipeIndex, self).prepare(object)
        self.prepared_data['tags'] = [rtag.name for rtag in object.tags.all()]
        return self.prepared_data