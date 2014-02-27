from constance import config
from django.views.generic import FormView, TemplateView
from haystack.views import SearchView

from recipes.models import Recipe, RecipeTag


class Home(TemplateView):
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        return {'featured_recipes': Recipe.objects.filter_featured(
                                    limit=config.FEATURED_RECIPE_COUNT),
                'newest_recipes': Recipe.objects.filter_newest(
                                    limit=config.NEWEST_RECIPE_COUNT),
                'tags': RecipeTag.objects.all()}
    

class RecipeSearch(FormView):
    def get(self, request, *args, **kwargs):
        return RecipeSearchHelper()(request)
    
    def post(self, request, *args, **kwargs):
        return RecipeSearchHelper()(request)
    
    '''
    # available methods from FormMixin
    get_initial(self)
    get_prefix(self)
    get_form_class(self)
    get_form(self, form_class)
    get_form_kwargs(self)
    get_success_url(self)
    form_valid(self, form)
    form_invalid(self, form)
    
    # and don't forget
    get_context_data(self, kwargs)
    post_context_data(self, kwargs)
    
    context_data expected:
       form, query, results
    '''

class RecipeSearchHelper(SearchView):
    def get_results(self):
        """ Overrides the parent method to sort results by popularity"""
        return self.form.search().order_by('-popularity')
