from django.views.generic import FormView, TemplateView

from organizations.forms import NoDonutsUserCreationForm


class NewUserCreation(FormView):
    form_class = NoDonutsUserCreationForm
    template_name = "organizations/new_user.html"


class PersonalProfile(TemplateView):
    """The user's view of their own profile"""
    template_name = "organizations/personal_profile.html"

