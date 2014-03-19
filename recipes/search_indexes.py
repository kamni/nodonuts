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
    serving_size = indexes.IntegerField(model_attr="serving_size")
    added_by = indexes.IntegerField(model_attr="added_by__id")
    is_public = indexes.BooleanField(model_attr="is_public")

    def get_model(self):
        return Recipe

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(date_added__lte=timezone.now())
    
    def prepare(self, object):
        self.prepared_data = super(RecipeIndex, self).prepare(object)
        self.prepared_data['tags'] = [rtag.name for rtag in object.tags.all()]
        return self.prepared_data