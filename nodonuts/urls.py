from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('recipes.urls')),
    url(r'^docs/', include('sphinxdoc.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, 'logout'),
    url(r'^site-manager/', include(admin.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
)
