from django import forms
from haystack.forms import SearchForm


class RecipeSearchForm(SearchForm):
    order = forms.ChoiceField(required=False, label="Sort Results By",
                              choices=(('popularity', 'popularity'),
                                       ('newest', 'newest'),
                                       ('alphabeta', 'alphabetical (A-Z)'),
                                       ('alphabetz', 'alphabetical (Z-A)')))
    
    def order_by(self, query, ordering=None):
        if ordering == 'newest':
            return query.order_by('-date_added')
        if ordering == 'alphabeta':
            return query.order_by('title')
        if ordering == 'alphabetz':
            return query.order_by('-title')
        if ordering == 'popularity' or ordering is None:
            return query.order_by('-popularity')
        return query
    
    def search(self):
        if not self.is_valid():
            return self.no_query_found()
        
        qstring = self.cleaned_data.get('q')
        ordering = self.cleaned_data.get('order')
        if not (qstring or ordering):
            return self.no_query_found()
        
        if qstring:
            query = self.searchqueryset.auto_query(qstring)
        else:
            query = self.searchqueryset.all()
            
        if self.load_all:
            query = query.load_all()

        return self.order_by(query, ordering)


'''
q = forms.CharField(required=False, label=_('Search'))

    def __init__(self, *args, **kwargs):
        self.searchqueryset = kwargs.pop('searchqueryset', None)
        self.load_all = kwargs.pop('load_all', False)

        if self.searchqueryset is None:
            self.searchqueryset = SearchQuerySet()

        super(SearchForm, self).__init__(*args, **kwargs)

    def no_query_found(self):
        """
        Determines the behavior when no query was found.

        By default, no results are returned (``EmptySearchQuerySet``).

        Should you want to show all results, override this method in your
        own ``SearchForm`` subclass and do ``return self.searchqueryset.all()``.
        """
        return EmptySearchQuerySet()

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            return self.no_query_found()

        sqs = self.searchqueryset.auto_query(self.cleaned_data['q'])

        if self.load_all:
            sqs = sqs.load_all()

        return sqs

    def get_suggestion(self):
        if not self.is_valid():
            return None

        return self.searchqueryset.spelling_suggestion(self.cleaned_data['q'])
class ModelSearchForm(SearchForm):
    def __init__(self, *args, **kwargs):
        super(ModelSearchForm, self).__init__(*args, **kwargs)
        self.fields['models'] = forms.MultipleChoiceField(choices=model_choices(), required=False, label=_('Search In'), widget=forms.CheckboxSelectMultiple)

    def get_models(self):
        """Return an alphabetical list of model classes in the index."""
        search_models = []

        if self.is_valid():
            for model in self.cleaned_data['models']:
                search_models.append(models.get_model(*model.split('.')))

        return search_models

    def search(self):
        sqs = super(ModelSearchForm, self).search()
        return sqs.models(*self.get_models())
'''