from django.conf.urls.defaults import *
from django.conf import settings
from django.shortcuts import render_to_response

urlpatterns = patterns('',
    # administration
    (r'^admin/', include('django.contrib.admin.urls')),

    # Using cab to browse software
    (r'^browse/', include('software.urls')),
    (r'^submit/', include('software.urls')),

    # Using registration
    (r'^accounts/', include('registration.urls')),
	(r'^forum/', include('djangoforum.urls')),
)

if settings.DEBUG and not settings.PRODUCTION:
	urlpatterns += patterns('',(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media'}),)
