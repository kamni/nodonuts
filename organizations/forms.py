from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

from organizations.models import UserProfile


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)


class NoDonutsAuthForm(AuthenticationForm):
    """Overrides the parent class 'username' to display as 'email'"""
    username = forms.EmailField(label=_('Email'))

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
    username = forms.EmailField(label=_('Email'))
    nickname = forms.CharField(label=_('Nickname'), required=True,
                               help_text="(A unique way for other users to identify you)")
    
    error_messages = {
        'duplicate_nickname': _("Another user already has this nickname. Please try another nickname."),
        'duplicate_username': _("Trying to log in? It looks like you already have an account."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    
    def clean_nickname(self):
        """Ensures the nickname is unique"""
        nickname = self.cleaned_data.get('nickname')
        if (UserProfile.objects.filter(nickname=nickname) or 
                User.objects.filter(username=nickname)):
            raise forms.ValidationError(self.error_messages['duplicate_nickname'],
                                        code='duplicate_nickname')
        return nickname
    
    def clean_username(self):
        """Overrides parent method to check for email uniqueness instead of username"""
        username = self.cleaned_data.get('username').lower()
        try:
            User._default_manager.get(email=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'],
                                    code='duplicate_username',)
    
    def save(self, commit=True):
        """Overrides parent method to handle new fields"""
        user = User.objects.create(username="user%d" % (User.objects.count() + 1),
                                        email=self.cleaned_data.get('username'))

        user.set_password(self.cleaned_data["password1"])
        user.save()
        
        profile = UserProfile.objects.create(user=user,
                                             nickname=self.cleaned_data.get('nickname'))
        return user
    