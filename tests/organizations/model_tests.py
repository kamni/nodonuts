from django.db import transaction, IntegrityError
from django.test import TestCase
from django_test_utils.model_utils import TestUser

from organizations.models import *


class UserProfileTests(TestCase):
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
        self.assertTrue(False, "Not Implemented")
    
    def test__unicode(self):
        self.assertTrue(False, "Not Implemented")