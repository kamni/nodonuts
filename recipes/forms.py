from django import forms
from django.contrib.auth.models import User
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from haystack.forms import SearchForm
from haystack.query import SQ

from recipes.models import Recipe, ServingSize


class NewRecipeForm(forms.ModelForm):
    added_by = forms.ModelChoiceField(queryset=User.objects.all(), 
                                      widget=forms.HiddenInput)
    
    class Meta:
        model = Recipe
        fields = ('title', 'short_description', 'image', 'serving_size',
                   'tags', 'ingredients', 'instructions', 'added_by')
    
    def _set_placeholder_text(self, field_dict):
        for field, placeholder in field_dict.items():
            self.fields[field].widget.attrs['placeholder'] = placeholder
    
    def __init__(self, added_by, *args, **kwargs):
        super(NewRecipeForm, self).__init__(*args, **kwargs)
        # the form seems to be ignoring the 'initial' param, so we're going to
        # manually set it
        if not kwargs.get('data'):
            self.fields['added_by'].initial = added_by
        self._set_placeholder_text({'title': 'Recipe Title',
                                    'short_description': 'Short Description',
                                    'ingredients': 'Ingredients with measurements, ' +
                                                   'one per line',
                                    'instructions': 'Instructions'})


class RecipeSearchForm(SearchForm):
    """TODO: docs and tests"""
    ORDERING_OPTIONS = (('popularity', 'popularity'),
                       ('newest', 'newest'),
                       ('alphabeta', 'alphabetical (A-Z)'),
                       ('alphabetz', 'alphabetical (Z-A)'))
                       
    q = forms.CharField(required=False, label=_('Search'),
                        widget=forms.TextInput(attrs={'placeholder': 
                                'Enter keywords, or leave blank to see all recipes'}))
    order = forms.ChoiceField(required=False, label="Sort Results By",
                              choices=ORDERING_OPTIONS)
    ss = forms.ChoiceField(required=False, label=_("Serving Size"),
                           choices=[(None, "-------")] + ServingSize.choices())
    tags = forms.CharField(required=False, label=_("Tags"),
                           widget=forms.TextInput(attrs={'placeholder':
                                                  'Tags separated by spaces'}))
    all = forms.BooleanField(label=_("Show Results From"), required=False,
                             widget=forms.RadioSelect(attrs={'value': False},
                                                      choices=((True, "everyone's recipes"),
                                                               (False, "my recipes"))))
    
    def __init__(self, *args, **kwargs):
        # TODO: tests
        
        # Forcing the form to initialize a True value for 'all' if one isn't
        # specified
        post_data = args[0].copy()
        post_data['all'] = post_data.get('all', True)
        args = (post_data,) + args[1:]
        return super(RecipeSearchForm, self).__init__(*args, **kwargs)
    
    def base_query_link(self):
        """TODO: docs and tests"""
        tags = urlquote(' '.join(self.tags)) if self.tags else ''
        ss = self.ss if self.ss else ''
        return ("?q=%s&amp;order=%s&amp;tags=%s&amp;ss=%s&amp;all=%s" % 
                (self.q, self.order, tags, ss, ['True', 'False'][bool(self.user)]))
    
    def order_by(self, query, ordering=None):
        # TODO: docs and tests
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
        # TODO: docs and tests
        if not self.is_valid():
            return self.no_query_found()
        
        self.q = self.cleaned_data.get('q')
        self.user = not self.cleaned_data.get('all') and self.user or None
        self.order = self.cleaned_data.get('order')
        self.tags = [tag.strip() for tag in self.cleaned_data.get('tags').split(' ') if tag.strip()]
        try:
            self.ss = int(self.cleaned_data.get('ss'))
        except ValueError:
            self.ss = None
        
        if self.q:
            query = self.searchqueryset.auto_query(self.q)
        else:
            query = self.searchqueryset.all()
        
        if self.user:
            query = query.filter(added_by=self.user)
        
        if self.ss is not None:
            query = query.filter(serving_size=self.ss)
            
        sq = SQ()
        for tag in self.tags:
            sq.add(SQ(tags=tag), SQ.AND)
        query = query.filter(sq)
        
        if self.load_all:
            query = query.load_all()

        return self.order_by(query, self.order).models(Recipe)
