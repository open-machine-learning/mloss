
from django.conf.urls import url, include

from blog.models import BlogItem
from blog.feeds import RssBlogFeed
from blog.feeds import BlogView
from blog.feeds import YearView
from blog.feeds import MonthView
from blog.feeds import DetailView


urlpatterns = [
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[A-Za-z0-9-_]+)/$', DetailView.as_view(), name='get_blog'),
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', MonthView.as_view()),
    url(r'^(?P<year>\d{4})/$', YearView.as_view()),
    url(r'^rss/latest/$', RssBlogFeed),
]
