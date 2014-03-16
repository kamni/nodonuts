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
        
        # if no nickname and no first/last name, return username
        user = User.objects.create(username="bazbar", email="bazbar@foobar.org")
        profile = TestUserProfile(user=user)
        TestUserSocialAuth(user=user, provider="google")
        self.assertEqual("bazbar", profile.profile_name())
        
        # if no nickname, return first/last name
        user = TestUser()
        profile = TestUserProfile(user=user)
        TestUserSocialAuth(user=user, provider="facebook")
        self.assertEqual(user.get_full_name(), profile.profile_name())
        
        # return nickname if it exists
        profile = TestUserProfile(nickname="cowabunga")
        TestUserSocialAuth(user=profile.user, provider="yahoo")
        self.assertEqual("cowabunga", profile.profile_name())
        
        # shouldn't error if no social auth
        profile = TestUserProfile()
        self.assertFalse(UserSocialAuth.objects.filter(user=profile.user))
        self.assert_(profile.profile_name())
    
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