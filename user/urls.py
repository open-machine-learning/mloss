
from django.conf.urls import url, include

from user.views import ShowUserList
from user.views import show_user
from user.views import update_user

# General softwares views.
urlpatterns = [
    url(r'^$', ShowUserList.as_view()),
    url(r'^view/(?P<user_id>\d+)/$', show_user),
    url(r'^update/(?P<user_id>\d+)/$', update_user),
]
