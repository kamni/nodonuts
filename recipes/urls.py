from django.conf.urls import patterns, include, url
from haystack.views import search_view_factory

from recipes.forms import RecipeSearchForm
from recipes.views import *


urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^search/$', search_view_factory(view_class=RecipeSearchView,
                                          form_class=RecipeSearchForm), 
                                          name='recipe_search'),
)