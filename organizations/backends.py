from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailAuthBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL using email instead of username.
    
    Note: while it is possible to create a custom User model in newer versions
        of Django, the python-social-auth does not play well with a custom
        User model. This is a workaround that allows us to authenticate using
        email without significant changes to existing forms and views. It most
        likely will not work if a custom User model is added later.
    """
    
    def authenticate(self, username=None, password=None, **kwargs):
        """
        For compatibility with ModelBackend, email comes from the username field.
        Returns None if the email/password combination don't match an
        existing user.
        
        :param username: valid email address
        :param password: password string
        :return: Django User or configured User subclass
        """
        # TODO: test
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get(email=username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)

