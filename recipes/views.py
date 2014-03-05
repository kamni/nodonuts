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
                'tags': RecipeTag.objects.filter_list(exclude_miscellaneous=True)}
    

class RecipeSearch(TemplateView):
    template_name = "search/search.html"
    
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
        """Overrides the parent method to sort results by popularity"""
        return self.form.search().order_by('-popularity')
    
    def extra_context(self):
        return {'tags': RecipeTag.objects.filter_list(exclude_miscellaneous=True)}

'''    
class SearchView(object):
    template = 'search/search.html'
    extra_context = {}
    query = ''
    results = EmptySearchQuerySet()
    request = None
    form = None
    results_per_page = RESULTS_PER_PAGE

    def __init__(self, template=None, load_all=True, form_class=None, 
                 searchqueryset=None, context_class=RequestContext, 
                 results_per_page=None):
        
        self.load_all = load_all
        self.form_class = form_class
        self.context_class = context_class
        self.searchqueryset = searchqueryset

        if form_class is None:
            self.form_class = ModelSearchForm

        if not results_per_page is None:
            self.results_per_page = results_per_page

        if template:
            self.template = template

    def __call__(self, request):
        """
        Generates the actual response to the search.

        Relies on internal, overridable methods to construct the response.
        """
        self.request = request

        self.form = self.build_form()
        self.query = self.get_query()
        self.results = self.get_results()

        return self.create_response()

    def build_form(self, form_kwargs=None):
        """
        Instantiates the form the class should use to process the search query.
        """
        data = None
        kwargs = {
            'load_all': self.load_all,
        }
        if form_kwargs:
            kwargs.update(form_kwargs)

        if len(self.request.GET):
            data = self.request.GET

        if self.searchqueryset is not None:
            kwargs['searchqueryset'] = self.searchqueryset

        return self.form_class(data, **kwargs)

    def get_query(self):
        """
        Returns the query provided by the user.

        Returns an empty string if the query is invalid.
        """
        if self.form.is_valid():
            return self.form.cleaned_data['q']

        return ''

    def get_results(self):
        """
        Fetches the results via the form.

        Returns an empty list if there's no query to search with.
        """
        return self.form.search()

    def build_page(self):
        """
        Paginates the results appropriately.

        In case someone does not want to use Django's built-in pagination, it
        should be a simple matter to override this method to do what they would
        like.
        """
        try:
            page_no = int(self.request.GET.get('page', 1))
        except (TypeError, ValueError):
            raise Http404("Not a valid number for page.")

        if page_no < 1:
            raise Http404("Pages should be 1 or greater.")

        start_offset = (page_no - 1) * self.results_per_page
        self.results[start_offset:start_offset + self.results_per_page]

        paginator = Paginator(self.results, self.results_per_page)

        try:
            page = paginator.page(page_no)
        except InvalidPage:
            raise Http404("No such page!")

        return (paginator, page)

    def extra_context(self):
        """
        Allows the addition of more context variables as needed.

        Must return a dictionary.
        """
        return {}

    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.
        """
        (paginator, page) = self.build_page()

        context = {
            'query': self.query,
            'form': self.form,
            'page': page,
            'paginator': paginator,
            'suggestion': None,
        }

        if self.results and hasattr(self.results, 'query') and self.results.query.backend.include_spelling:
            context['suggestion'] = self.form.get_suggestion()

        context.update(self.extra_context())
        return render_to_response(self.template, context, context_instance=self.context_class(self.request))
'''
