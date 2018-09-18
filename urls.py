from django.views.static import serve
from django.conf.urls import url, include
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import admin
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views.generic import RedirectView

from forshow.views import newsindex
from forshow.views import faqindex

admin.autodiscover()

urlpatterns = [
    # administration
    url(r'^admin/', include(admin.site.urls)),

    # software and revision
    url(r'^software/', include('software.urls')),
    url(r'^revision/', include('revision.urls')),

    # Using registration
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^community/', include('community.urls')),
    url(r'^user/', include('user.urls')),


    # Display News and FAQ- simplest possible dynamic page
    url(r'^news/', newsindex),
    url(r'^faq/', faqindex),

    # redirect the root to news
    url(r'^$', RedirectView.as_view(url='/software/')),

    # Enable comments
    url(r'^comments/', include('django_comments.urls')),
]

if settings.DEBUG and not settings.PRODUCTION:
    urlpatterns += [url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),]
