"""
URLConf for Django-Forum.

django-forum assumes that the forum application is living under
/forum/.

Usage in your base urls.py:
	(r'^forum/', include('community.urls')),

"""

from django.conf.urls.defaults import *
from community.models import Forum

forum_dict = {
	'queryset' : Forum.objects.all(),
}

urlpatterns = patterns('',
	(r'^$', 'django.views.generic.list_detail.object_list', forum_dict),
	(r'^(?P<slug>[A-Za-z0-9-_]+)/$', 'community.views.forum'),
	(r'^rss/(?P<forum>[A-Za-z0-9-_]+)/$', 'community.feeds.ForumFeed'),
	(r'^rss/(?P<forum>[A-Za-z0-9-_]+)/(?P<thread>[0-9]+)/$', 'community.feeds.ThreadFeed'),
	(r'^(?P<forum>[A-Za-z0-9-_]+)/(?P<thread>[0-9]+)/$', 'community.views.thread'),
	(r'^(?P<forum>[A-Za-z0-9-_]+)/new/$', 'community.views.newthread'),
	(r'^(?P<forum>[A-Za-z0-9-_]+)/(?P<thread>[0-9]+)/reply/$', 'community.views.reply'),
)
