from requests import request, HTTPError

from django.core.files.base import ContentFile

from organizations.models import UserProfile


def save_profile_image(strategy, user, response, details, *args, **kwargs):
    # TODO: docs and tests
    profile = UserProfile.objects.get_or_create(user=user)[0]
    
    is_new = kwargs.get('is_new', False) or not profile.avatar_url
    if is_new and strategy.backend.name == 'facebook':
        profile.avatar_url = ('http://graph.facebook.com/{0}/picture'.format(response['id']) +
                              '?type=large')
        profile.save()
    else:
        pass