from django.conf.urls import patterns, include, url

from site_manager.views import *


urlpatterns = patterns('',
    url(r'^$', AdminPanel.as_view(), name='admin_panel'),
)