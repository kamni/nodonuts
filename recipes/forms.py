from django import forms
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from haystack.forms import SearchForm
from haystack.query import SQ

from recipes.models import Recipe, ServingSize


class RecipeSearchForm(SearchForm):
    """TODO: docs and tests"""
    q = forms.CharField(required=False, label=_('Search'),
                        widget=forms.TextInput(attrs={'placeholder': 
                                'Enter search terms, or leave blank to see all recipes'}))
    order = forms.ChoiceField(required=False, label="Sort Results By",
                              choices=(('popularity', 'popularity'),
                                       ('newest', 'newest'),
                                       ('alphabeta', 'alphabetical (A-Z)'),
                                       ('alphabetz', 'alphabetical (Z-A)')))
    ss = forms.ChoiceField(required=False, label="Serving Size",
                           choices=[(None, "-------")] + ServingSize.choices())
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs = {'placeholder':
                                'Tags separated by spaces'}))
    
    def base_query_link(self):
        """TODO: docs and tests"""
        tags = urlquote(' '.join(self.tags)) if self.tags else ''
        ss = self.ss if self.ss else ''
        return "?q=%s&amp;order=%s&amp;tags=%s&amp;ss=%s" % (self.q, self.order, 
                                                             tags, ss)
    
    def order_by(self, query, ordering=None):
        if ordering == 'newest':
            return query.order_by('-date_added')
        if ordering == 'alphabeta':
            return query.order_by('title')
        if ordering == 'alphabetz':
            return query.order_by('-title')
        if ordering == 'popularity' or not ordering:
            return query.order_by('-popularity')
        return query
    
    def search(self):
        if not self.is_valid():
            return self.no_query_found()
        
        self.q = self.cleaned_data.get('q')
        self.order = self.cleaned_data.get('order')
        self.tags = [tag.strip() for tag in self.cleaned_data.get('tags').split(' ') if tag.strip()]
        try:
            self.ss = int(self.cleaned_data.get('ss'))
        except ValueError:
            self.ss = None
        
        if not (self.q or self.order or self.tags or self.ss is not None):
            return self.no_query_found()
        
        if self.q:
            query = self.searchqueryset.auto_query(self.q)
        else:
            query = self.searchqueryset.all()
            
        if self.ss is not None:
            query = query.filter(serving_size=self.ss)
            
        sq = SQ()
        for tag in self.tags:
            sq.add(SQ(tags=tag), SQ.AND)
        query = query.filter(sq)
        
        if self.load_all:
            query = query.load_all()

        return self.order_by(query, self.order).models(Recipe)
