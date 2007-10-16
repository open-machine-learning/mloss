from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.models import User
from django.views.generic.list_detail import object_list



user_info_dict = dict(paginate_by=10,
                      queryset=User.objects.all(),
                      template_name='software/user_list.html')


urlpatterns = patterns('',
    # administration
    (r'^admin/', include('django.contrib.admin.urls')),

    # Using cab to browse software
    (r'^software/', include('software.urls')),
    (r'^users/$', object_list, user_info_dict),
    (r'^users/(?P<username>[^/]+)/$', 'software.views.entry.software_by_user'),

    # Using registration
    (r'^accounts/', include('registration.urls')),
    (r'^community/', include('community.urls')),

    # Display News and FAQ- simplest possible dynamic page
    (r'^news/', 'forshow.views.newsindex'),
    (r'^faq/', 'forshow.views.faqindex'),

    # redirect the root to news
    #('^$', 'forshow.views.newsindex'),
    ('^$', 'django.views.generic.simple.redirect_to', {'url':'/about/'}),

    # Enable comments
    (r'^comments/', include('django.contrib.comments.urls.comments')),

)

if settings.DEBUG and not settings.PRODUCTION:
	urlpatterns += patterns('',(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media'}),)
