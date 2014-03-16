from django.views.generic import TemplateView


class PersonalProfile(TemplateView):
    """The user's view of their own profile"""
    template_name = "organizations/personal_profile.html"
