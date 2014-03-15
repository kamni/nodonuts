from constance import config
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('recipes.urls')),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, 'logout'),
    url(r'^site-manager/django/', include(admin.site.urls)),
    url(r'^site-manager/', include('site_manager.urls')),
    url(r'^textedit/', include('scribbler.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
)

if settings.INCLUDE_DOC_URLS:
    urlpatterns += (url(r'^docs/', include('sphinxdoc.urls')),)

if config.DISPLAY_TERMS_AND_CONDITIONS:
    urlpatterns += (url(r'^terms-and-conditions/$', TemplateView.as_view(template_name="toc.html"), name="terms"),)

if config.DISPLAY_PRIVACY_POLICY:
    urlpatterns += (url(r'^privacy-policy/$', TemplateView.as_view(template_name="privacy.html"), name="privacy"),)