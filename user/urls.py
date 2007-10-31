from django.conf.urls.defaults import *

# General softwares views.
urlpatterns = patterns('',
    (r'^$', 'user.views.show_user_list'),
    (r'^view/(?P<user_id>\d+)/$', 'user.views.show_user'),
    (r'^update/(?P<user_id>\d+)/$', 'user.views.update_user'),
)
