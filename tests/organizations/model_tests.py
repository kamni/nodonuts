import random
try:
    import json
except ImportError:
    import simplejson as json

from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.test import TestCase
from django_test_utils.model_utils import TestUser
from django_test_utils.random_generators import random_uid

from organizations.models import *


class UserProfileTests(TestCase):
    def test_get_avatar(self):
        self.assertTrue(False, "Not Implemented")
    
    def test_get_social_logins(self):
        # no social logins
        profile = TestUserProfile()
        self.assertEqual([], profile.get_social_logins())
        
        # multiple social logins
        for provider in ('google', 'yahoo'):
            TestUserSocialAuth(user=profile.user, provider=provider)
        logins = profile.get_social_logins()
        self.assertEqual(2, len(logins))
        self.assertTrue('google' in logins)
        self.assertTrue('yahoo' in logins)
    
    def test_profile_name(self):
        # should return username if user has a twitter login
        user = TestUser(username="foo_bar_baz")
        profile = TestUserProfile(user=user, nickname="fooby")
        TestUserSocialAuth(user=user, provider='twitter')
        self.assertEqual("foo_bar_baz", profile.profile_name())
        
        # users with another social login should prefer nickname, but have a
        # username that was imported
        for social_auth in ('google', 'yahoo', 'facebook'):
            user = TestUser(username="%s_user" % social_auth)
            profile = TestUserProfile(user=user)
            TestUserSocialAuth(user=user, provider=social_auth)
            self.assertEqual("%s_user" % social_auth, profile.profile_name())
            
            profile.nickname = "%sNick" % social_auth
            self.assertEqual("%sNick" % social_auth, profile.profile_name())
        
        # for other users, prefer nickname, but return 'User' if no nickname
        # is set
        profile = TestUserProfile()
        self.assertEqual('User', profile.profile_name())
        profile.nickname = 'PlainOldUser'
        self.assertEqual('PlainOldUser', profile.profile_name())
    
    def test__init(self):
        # all fields
        user1 = TestUser()
        self.assert_(UserProfile.objects.create(user=user1, nickname="foobar",
                                                avatar="test.jpg"))
        
        # minimum required fields
        self.assert_(UserProfile.objects.create(user=TestUser()))
        
        # user is required
        with transaction.atomic():
            self.assertRaises(IntegrityError, UserProfile.objects.create)
        
        # user must be unique
        with transaction.atomic():
            self.assertRaises(IntegrityError, UserProfile.objects.create,
                              user=user1)
    
    def test__repr(self):
        user = TestUser()
        profile = TestUserProfile(user=user)
        self.assertEquals("<UserProfile: %s>" % user, repr(profile))
    
    def test__unicode(self):
        profile = TestUserProfile()
        self.assertEquals(unicode(profile.profile_name()), unicode(profile))


############# Test Models ################

def TestUserProfile(user=None, nickname=None, avatar=None):
    return UserProfile.objects.create(user=user or TestUser(),
                                      nickname=nickname,
                                      avatar=avatar)


def TestUserSocialAuth(user=None, provider=None, uid=None, extra_data=None):
    provider = provider or random.choice(['facebook', 'google', 
                                          'twitter', 'yahoo'])
    return UserSocialAuth.objects.create(user=user or TestUser(),
                                         provider=provider,
                                         uid=uid or random_uid(),
                                         extra_data=extra_data or json.dumps({}))