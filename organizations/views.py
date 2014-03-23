from constance import config
from django.contrib import auth
from django.core import urlresolvers
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, FormView, UpdateView

from organizations.forms import EditProfileForm, NoDonutsUserCreationForm
from organizations.models import UserProfile
from recipes.forms import NewRecipeForm
from recipes.models import Recipe


class EditProfile(UpdateView):
    template_name = "organizations/edit_profile.html"
    form_class = EditProfileForm
    
    def post(self, request, *args, **kwargs):
        from django.http import HttpResponse
        try:
            response = super(EditProfile, self).post(request, *args, **kwargs)
            return HttpResponse('edit-success')
        except Exception, e:
            #return HttpResponse(str(e))
            return HttpResponse('edit-fail')
    
    def get_object(self):
        # TODO: test
        profile = get_object_or_404(UserProfile, user=self.request.user)
        if 'twitter' in profile.get_social_logins():
            # Twitter users need to go to Twitter to edit their own profiles,
            # as per the Twitter developer agreement
            raise Http404
        return profile
    
    def get_success_url(self):
        return urlresolvers.reverse('my_profile')


class NewUserCreation(FormView):
    # TODO: docs, tests
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


class PersonalProfile(CreateView):
    """The user's view of their own profile"""
    template_name = "organizations/personal_profile.html"
    form_class = NewRecipeForm
    
    def get(self, request, *args, **kwargs):
        from django.http import HttpResponse
        try:
            response = super(PersonalProfile, self).get(request, *args, **kwargs)
            return HttpResponse('profile-success')
        except Exception, e:
            #return HttpResponse(str(e))
            return HttpResponse('profile-fail')
    
    def get_context_data(self, **kwargs):
        # this is following the search page's results so we can reuse
        # the template
        kwargs.update({'page': {'object_list': self._recipe_results()}})
        return kwargs
    
    def get_form(self, form_class):
        return form_class(added_by=self.request.user, **self.get_form_kwargs())
    
    def get_success_url(self):
        # redirect to the same page
        return urlresolvers.reverse('my_profile')
    
    def _recipe_results(self):
        """
        Returns a list of dictionaries for a filtered search of the user's recipes.
        
        :return: list of dictionaries
        """
        results = Recipe.objects.filter(added_by=self.request.user
                               ).order_by('-date_added')[:config.USER_NEWEST_RECIPE_COUNT]
        return [{'object': result} for result in results]

