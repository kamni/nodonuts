from django.core.exceptions import ValidationError


def one_or_negative_one(value):
    """ Validates that the value is either 1 or -1. Used for Ratings """
    if value not in (1, -1):
        raise ValidationError("This field can only take values of 1 or -1")
    return value