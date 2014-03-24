from django.conf import settings
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
    avatar_url = models.URLField(blank=True, null=True,
                                 help_text="Alternative to an uploaded file")
    
    def get_avatar(self, large=True):
        """
        Retrieves the image url to use for this particular user.
        If avatar is not set, returns a default image.
        
        :return: string
        """
        avatar_url = self.avatar_url
        try:
            login = self.get_social_logins()[0]
        except IndexError:
            login = None
        if login == 'facebook' and avatar_url:
            if large:
                avatar_url += '?type=large'
                
        avatar = self.avatar.url if self.avatar else None
        return (avatar_url or avatar or 
                "/".join((settings.STATIC_URL, "img", "avatar.png")))
    
    def get_social_logins(self):
        """
        Returns a list of names of all social media logins for the user
        
        :return: list of strings
        """
        return [auth['provider'] for auth in self.user.social_auth.values('provider')]
    
    def profile_name(self):
        """
        Returns the name that should be used for the displaying the user.
        If the user has a social media login with Twitter, that display name 
        need to take priority, as per their developer agreement.
        
        :return: string
        """
        social_logins = self.get_social_logins()
        if 'twitter' in social_logins:
            return self.user.username
        elif social_logins:
            return self.user.get_full_name()
        
        # Users without a social login have a randomly generated, meaningless
        # username, so if they don't have a nickname then we'll assume they're
        # either from an older version of NoDonuts or were generated from the
        # command line and need a user-friendly display name
        return self.nickname or "User"
    
    def __repr__(self):
        return "<UserProfile: %s>" % self.user
    
    def __unicode__(self):
        return unicode(self.profile_name())
