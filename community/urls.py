"""
URLConf for Django-Forum.

django-forum assumes that the forum application is living under
/forum/.

Usage in your base urls.py:
	(r'^forum/', include('community.urls')),

"""

from django.conf.urls import patterns, include
from community.models import Forum
from aggregator.models import FeedItem
from community.summary import get_latest_news
from django.views.generic.list import ListView

forum_dict = {
    'queryset' : Forum.objects.all(),
#    'extra_context' : get_latest_news()
}

comm1_dict = {
    'template_name' : 'community/community1.html',
    'queryset' : Forum.objects.all(),
#    'extra_context' : get_latest_news()
}

comm2_dict = {
    'template_name' : 'community/community2.html',
    'queryset' : FeedItem.objects.all(),
#    'extra_context' : get_latest_news()
}



urlpatterns = patterns('',
	(r'^$', 'community.views.get_summary_page'),
	(r'^forum/$', ListView.as_view(**forum_dict)),
	(r'^blog/', include('blog.urls')),
	(r'^(?P<slug>[A-Za-z0-9-_]+)/$', 'community.views.forum'),
	(r'^rss/(?P<forum>[A-Za-z0-9-_]+)/$', 'community.feeds.ForumFeed'),
	(r'^rss/(?P<forum>[A-Za-z0-9-_]+)/(?P<thread>[0-9]+)/$', 'community.feeds.ThreadFeed'),
	(r'^subscribe/(?P<forum>[A-Za-z0-9-_]+)/$', 'community.subscriptions.SubscribeForum'),
	(r'^subscribe/(?P<forum>[A-Za-z0-9-_]+)/(?P<thread>[0-9]+)/$', 'community.subscriptions.SubscribeThread'),
	(r'^bookmark/(?P<forum>[A-Za-z0-9-_]+)/$', 'community.subscriptions.BookmarkForum'),
	(r'^bookmark/(?P<forum>[A-Za-z0-9-_]+)/(?P<thread>[0-9]+)/$', 'community.subscriptions.BookmarkThread'),
	(r'^unsubscribe/(?P<forum>[A-Za-z0-9-_]+)/$', 'community.subscriptions.UnsubscribeForum'),
	(r'^unsubscribe/(?P<forum>[A-Za-z0-9-_]+)/(?P<thread>[0-9]+)/$', 'community.subscriptions.UnsubscribeThread'),
	(r'^rmbookmark/(?P<forum>[A-Za-z0-9-_]+)/$', 'community.subscriptions.RemoveBookmarkForum'),
	(r'^rmbookmark/(?P<forum>[A-Za-z0-9-_]+)/(?P<thread>[0-9]+)/$', 'community.subscriptions.RemoveBookmarkThread'),
	(r'^(?P<forum>[A-Za-z0-9-_]+)/(?P<thread>[0-9]+)/$', 'community.views.thread'),
	(r'^(?P<forum>[A-Za-z0-9-_]+)/new/$', 'community.views.newthread'),
	(r'^(?P<forum>[A-Za-z0-9-_]+)/(?P<thread>[0-9]+)/reply/$', 'community.views.reply'),
)
