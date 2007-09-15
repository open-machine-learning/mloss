from django.conf.urls.defaults import *
from static import *

urlpatterns = patterns('',
    # home page
    (r'^$', about),

    # administration
    (r'^admin/', include('django.contrib.admin.urls')),

    # Using cab to browse software
    (r'^browse/', include('software.urls')),
    (r'^submit/', include('software.urls')),

    # static pages
    (r'^workshop/$', workshop),
    (r'^links/$', links),
    (r'^faq/$', faq),
    (r'^about/$', about),

    # Using registration
    #(r'^accounts/', include('registration.urls')),
)


