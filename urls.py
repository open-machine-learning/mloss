from django.conf.urls.defaults import *
from django.conf import settings
from django.shortcuts import render_to_response
from django.views.generic.simple import redirect_to

urlpatterns = patterns('',
    # administration
    (r'^admin/', include('django.contrib.admin.urls')),

    # Using cab to browse software
    (r'^software/', include('software.urls')),

    # Using registration
    (r'^accounts/', include('registration.urls')),
    (r'^community/', include('djangoforum.urls')),

    # Display News and FAQ- simplest possible dynamic page
    #(r'^news/', 'forshow.views.newsindex'),
    (r'^faq/', 'forshow.views.faqindex'),

    # redirect the root to news
    ('^$', 'forshow.views.newsindex'),
)

if settings.DEBUG and not settings.PRODUCTION:
	urlpatterns += patterns('',(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media'}),)
