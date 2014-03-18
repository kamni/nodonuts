from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _


class NoDonutsAuthForm(AuthenticationForm):
    """Overrides the parent class 'username' to display as 'email'"""
    username = forms.CharField(label=_("Email"), max_length=254)

    error_messages = {
        'invalid_login': _("Please enter a correct email and password. "
                           "Note that password is case-sensitive."),
        'inactive': _("This account is inactive."),
    }  
 
    
class NoDonutsUserCreationForm(UserCreationForm):
    """
    Custom user creation form for NoDonuts.
    Sets the 'username' to email and creates a system-only username. Also
    allows setting the display name.
    """
    # username is email field
    # add a display name
    # create profile
    