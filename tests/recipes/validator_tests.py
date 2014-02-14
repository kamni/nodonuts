from django.core.exceptions import ValidationError
from django.test import TestCase

from recipes.validators import *


class ValidatorTests(TestCase):
    def test_one_or_negative_one(self):
        for i in range (-10, 11):
            if i in (-1, 1):
                self.assertEquals(i, one_or_negative_one(i))
            else:
                self.assertRaises(ValidationError, one_or_negative_one, i)