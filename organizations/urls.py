from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from organizations.views import *


urlpatterns = patterns('',
    url(r'^my-profile/$', login_required(PersonalProfile.as_view()), name='my_profile'),
    url(r'^new-user/$', NewUserCreation.as_view(), name='new_user'),
)