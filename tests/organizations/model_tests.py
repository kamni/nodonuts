from django.db import transaction, IntegrityError
from django.test import TestCase
from django_test_utils.model_utils import TestUser

from organizations.models import *


class UserProfileTests(TestCase):
    def test_get_avatar(self):
        self.assertTrue(False, "Not Implemented")
    
    def test_profile_name(self):
        self.assertTrue(False, "Not Implemented")
    
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


def TestUserProfile(user=None, nickname=None, avatar=None):
    return UserProfile.objects.create(user=user or TestUser(),
                                      nickname=nickname,
                                      avatar=avatar)