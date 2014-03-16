from django.contrib.auth.models import User
from django.db import models
from social.apps.django_app.default.models import UserSocialAuth


class UserProfile(models.Model):
    """
    Stores additional information related to the user.
    
    :field user: ForeignKey to User, unique
    :field nickname: CharField, max length 20, nullable, unique if not null
    :field avatar: ImageField, nullable
    """
    user = models.ForeignKey(User, unique=True)
    nickname = models.CharField(max_length=20, blank=True, null=True,
                                help_text="Display name for user")
    avatar = models.ImageField(upload_to='organizations/avatars', blank=True,
                               null=True, help_text="Image to display for user " +
                               "profile")
    
    def get_avatar(self):
        """
        Retrieves the image url to use for this particular user.
        If avatar is not set, returns a default image.
        
        :return: string
        """
        # TODO: implement and test
        return None
    
    def get_social_logins(self):
        """
        Returns a list of names of all social media logins for the user
        
        :return: list of strings
        """
        return [auth['provider'] for auth in UserSocialAuth.objects.filter(user=self.user)]
    
    def profile_name(self):
        """
        Returns the name that should be used for the displaying the user.
        If the user has a social media login with Twitter, that display name 
        need to take priority, as per their developer agreement.
        
        :return: string
        """
        if 'twitter' in self.get_social_logins():
            return self.user.username
        
        return self.nickname or self.user.get_full_name() or self.user.username
    
    def __repr__(self):
        return "<UserProfile: %s>" % self.user
    
    def __unicode__(self):
        return unicode(self.profile_name())
