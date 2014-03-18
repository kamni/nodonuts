from organizations.models import UserProfile


def profile(request):
    """
    Gets the UserProfile associated with the currently logged-in user.
    Creates the UserProfile if the user does not already have one; if the user 
    isn't logged in, returns None.
    
    :param request: Django request object
    :return: UserProfile
    """
    # TODO: tests
    if request.user.is_authenticated():
        return {'profile': UserProfile.objects.get_or_create(user=request.user)[0]}
    return {}