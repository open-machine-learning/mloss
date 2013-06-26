from django.conf.urls import patterns, include
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import admin
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = patterns('',
    # administration
    #(r'^admin/(.*)', admin.site.root),
    (r'^admin/', include(admin.site.urls)),

    # software and revision
    (r'^software/', include('software.urls')),
    (r'^revision/', include('revision.urls')),

    # Using registration
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^community/', include('community.urls')),
    (r'^user/', include('user.urls')),

    # Display News and FAQ- simplest possible dynamic page
    (r'^news/', 'forshow.views.newsindex'),
    (r'^faq/', 'forshow.views.faqindex'),

    # redirect the root to news
    #('^$', 'forshow.views.newsindex'),
    ('^$', RedirectView.as_view(url='/software/')),

    # Enable comments
    (r'^comments/', include('django.contrib.comments.urls')),
)

if settings.DEBUG and not settings.PRODUCTION:
    urlpatterns += patterns('',(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media'}),)
