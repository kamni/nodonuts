from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('recipes.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^site-manager/', include(admin.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
)
