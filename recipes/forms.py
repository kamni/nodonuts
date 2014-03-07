from django import forms
from django.utils.translation import ugettext_lazy as _
from haystack.forms import SearchForm

from recipes.models import ServingSize


class RecipeSearchForm(SearchForm):
    """TODO: docs and tests"""
    q = forms.CharField(required=False, label=_('Search'),
                        widget=forms.TextInput(attrs={'placeholder': 
                                                      'Enter search terms, ' +
                                                      'or leave blank to see ' +
                                                      'all recipes'}))
    order = forms.ChoiceField(required=False, label="Sort Results By",
                              choices=(('popularity', 'popularity'),
                                       ('newest', 'newest'),
                                       ('alphabeta', 'alphabetical (A-Z)'),
                                       ('alphabetz', 'alphabetical (Z-A)')))
    ss = forms.ChoiceField(required=False, label="Serving Size",
                           choices=[(None, "-------")] + ServingSize.choices())
    
    def base_query_link(self):
        """TODO: docs and tests"""
        return "?q=%s&amp;order=%s&amp;ss=%s" % (self.q, self.order, 
                                                 self.ss if self.ss is not None
                                                 else '')
    
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
        
        self.q = self.cleaned_data.get('q')
        self.order = self.cleaned_data.get('order')
        try:
            self.ss = int(self.cleaned_data.get('ss'))
        except ValueError:
            self.ss = None
        
        if not (self.q or self.order or self.ss is not None):
            return self.no_query_found()
        
        if self.q:
            query = self.searchqueryset.auto_query(self.q)
        else:
            query = self.searchqueryset.all()
            
        if self.ss is not None:
            query = query.filter(serving_size=self.ss)
        
        if self.load_all:
            query = query.load_all()

        return self.order_by(query, self.order)
