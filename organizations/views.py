from django.contrib import auth
from django.core import urlresolvers
from django.views.generic import FormView, TemplateView

from organizations.forms import NoDonutsUserCreationForm


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


class PersonalProfile(TemplateView):
    """The user's view of their own profile"""
    template_name = "organizations/personal_profile.html"

