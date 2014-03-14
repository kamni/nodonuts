from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import user_passes_test

from site_manager.views import *


admin_only = user_passes_test(lambda user: user.is_superuser)

urlpatterns = patterns('',
    url(r'^$', admin_only(AdminPanel.as_view()), name='admin_panel'),
)