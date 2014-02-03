from django.conf.urls import patterns, include, url

from recipes.views import *


urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    
)