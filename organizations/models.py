from django.contrib.auth.models import User
from django.db import models


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
    
    def profile_name(self):
        """
        Returns the name that should be used for the displaying the user.
        If the user has a social media login, that display name takes priority.
        
        :return: string
        """
        # TODO: implement and test
        return None
    
    def __repr__(self):
        return "<UserProfile: %s>" % self.user
    
    def __unicode__(self):
        return unicode(self.profile_name())
