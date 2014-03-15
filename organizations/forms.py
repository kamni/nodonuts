from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext, ugettext_lazy as _


class NoDonutsAuthForm(AuthenticationForm):
    """Overwrites the parent class 'username' to display as 'email'"""
    username = forms.CharField(label=_("Email"), max_length=254)

    error_messages = {
        'invalid_login': _("Please enter a correct email and password. "
                           "Note that password is case-sensitive."),
        'inactive': _("This account is inactive."),
    }