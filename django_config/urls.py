from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('recipes.urls')),
    url(r'^site-manager/', include(admin.site.urls)),
)
