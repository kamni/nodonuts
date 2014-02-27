from django.views.generic import FormView, TemplateView
from haystack.views import SearchView


class Home(TemplateView):
    template_name = "home.html"
    

class RecipeSearch(FormView):
    def get(self, request, *args, **kwargs):
        return SearchView()(request)
    
    def post(self, request, *args, **kwargs):
        return SearchView()(request)
