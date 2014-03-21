from constance import config
from django.contrib import auth
from django.core import urlresolvers
from django.views.generic import FormView, TemplateView

from organizations.forms import NoDonutsUserCreationForm
from recipes.forms import NewRecipeForm
from recipes.models import Recipe


class NewUserCreation(FormView):
    form_class = NoDonutsUserCreationForm
    template_name = "organizations/new_user.html"
    
    def form_valid(self, form):
        user = form.save()
        user_cache = auth.authenticate(username=user.email, 
                                       password=form.cleaned_data.get('password1'))
        
        if user_cache is None or not user_cache.is_active:
            # this should not happen unless there is a hacking attempt
            raise Exception("Invalid attempt to log in after sign-up.")
            
        auth.login(self.request, user_cache)    
        return super(NewUserCreation, self).form_valid(form)
    
    def get_success_url(self):
        return urlresolvers.reverse('my_profile')


class PersonalProfile(FormView):
    """The user's view of their own profile"""
    template_name = "organizations/personal_profile.html"
    form_class = NewRecipeForm
    
    def form_invalid(self, form):
        import pdb; pdb.set_trace()
        super(PersonalProfile, self).form_invalid(form)
    
    def form_valid(self, form):
        recipe = form.save()
        import pdb; pdb.set_trace()
        super(PersonalProfile, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        # this is following the search page's results so we can reuse
        # the template
        kwargs.update({'page': {'object_list': self._recipe_results()}})
        return kwargs
    
    def get_form(self, form_class):
        return form_class(added_by=self.request.user, **self.get_form_kwargs())
    
    def _recipe_results(self):
        """
        Returns a list of dictionaries for a filtered search of the user's recipes.
        
        :return: list of dictionaries
        """
        results = Recipe.objects.filter(added_by=self.request.user
                               ).order_by('-date_added')[:config.USER_NEWEST_RECIPE_COUNT]
        return [{'object': result} for result in results]

