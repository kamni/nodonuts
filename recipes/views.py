import re

from constance import config
from django.views.generic import FormView, TemplateView
from haystack.views import SearchView

from recipes.models import Recipe, RecipeTag


class Home(TemplateView):
    """The first page that users see when they visit the site"""
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        return {'featured_recipes': Recipe.objects.filter_featured(
                                    limit=config.FEATURED_RECIPE_COUNT),
                'newest_recipes': Recipe.objects.filter_newest(
                                    limit=config.NEWEST_RECIPE_COUNT),
                'tags': RecipeTag.objects.filter_list(exclude_miscellaneous=False)}
    

class RecipeSearchView(SearchView):
    """Primary search page for recipes. Uses Haystack."""
    results_per_page = config.SEARCH_RESULTS_PER_PAGE
    
    def build_form(self, *args, **kwargs):
        form = super(RecipeSearchView, self).build_form(*args, **kwargs)
        user = self.request.user
        form.user = user.id if user.is_authenticated() else None
        return form
    
    def get_selected_tags(self):
        """Determines which tags should show up as 'selected' in the view"""
        # TODO: test
        return self.form.tags
    
    def extra_context(self):
        # TODO: test
        return {'is_search': True,
                'tags': RecipeTag.objects.filter_list(exclude_miscellaneous=False),
                'selected_tags': self.get_selected_tags(),
                'order': self.request.GET.get('order')}
