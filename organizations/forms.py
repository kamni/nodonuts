from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

from organizations.models import UserProfile


class EditProfileForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(),
                                  widget=forms.HiddenInput)
    email = forms.EmailField(required=False)
    old_password = forms.CharField(required=False, widget=forms.PasswordInput)
    new_password1 = forms.CharField(required=False, widget=forms.PasswordInput)
    new_password2 = forms.CharField(required=False, widget=forms.PasswordInput)
    
    error_messages = {
        'password_needed': _("Please enter your currrent password to change " +
                             "this information"),
        'wrong_password': _("Incorrect password"),
        'password_mismatch': _("The new passwords don't match"),
        'duplicate_email': _("This email address is already taken")
    }
    
    class Meta:
        model = UserProfile
        
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        if not kwargs.get('data'):
            self.fields['email'].initial = self.instance.user.email
    
    def clean_email(self):
        # TODO: test
        email = self.cleaned_data.get('email')
        old_password = self.cleaned_data.get('old_password')
        
        if email and not old_password:
            raise ValidationError(self.error_messages['password_needed'])
        if not self.instance.user.check_password(old_password):
            raise ValidationError(self.error_messages['wrong_password'])
        if User.objects.filter(email=email).exclude(id=self.instance.user.id):
            raise ValidationError(self.error_messages['duplicate_email'])
        
        return email

    def clean_new_password1(self):
        # TODO: test
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        old_password = self.cleaned_data.get('old_password')
     
        if new_password1 and not old_password:
            raise ValidationError(self.error_messages['password_needed'])
        if not self.instance.user.check_password(old_password):
            raise ValidationError(self.error_messages['wrong_password'])
        if new_password1 != new_password2:
            raise ValidationError(self.error_messages['password_mismatch'])
        
        return new_password1
    
    def clean_nickname(self):
        # TODO: test
        profile = self.instance
        nickname = self.cleaned_data.get('nickname')
        if nickname:
            if (UserProfile.objects.filter(nickname=nickname).exclude(id=profile.id) or
                    User.objects.filter(username=nickname).exclude(id=profile.user.id)):
                raise forms.ValidationError("Another user already has this " +
                                            "nickname. Please try another nickname.")
        return nickname
    
    def save(self, *args, **kwargs):
        # TODO: test
        profile = super(EditProfileForm, self).save(*args, **kwargs)
        user = profile.user
        
        email = self.cleaned_data.get('email')
        if email:
            user.email = email
        
        password = self.cleaned_data.get('new_password1')
        if password:
            user.set_password(password)
        
        if email or password:
            user.save()
        
        return profile


class NoDonutsAuthForm(AuthenticationForm):
    """Overrides the parent class 'username' to display as 'email'"""
    username = forms.EmailField(label=_('Email'))

    error_messages = {
        'invalid_login': _("Please enter a correct email and password. "
                           "Note that password is case-sensitive."),
        'inactive': _("This account is inactive.")}  
 
    
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
    