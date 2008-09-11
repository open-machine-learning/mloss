from django.conf.urls.defaults import *
from blog.models import BlogItem
from blog.feeds import RssBlogFeed
from community.summary import get_latest_news

info_dict = {
    'queryset' : BlogItem.objects.all(),
    'date_field' : 'pub_date',
    'extra_context' : get_latest_news()
}


urlpatterns = patterns('django.views.generic.date_based',
   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[A-Za-z0-9-_]+)/$', 'object_detail', dict(info_dict, slug_field='slug')),
   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'archive_day', info_dict),
   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'archive_month', info_dict),
   (r'^(?P<year>\d{4})/$', 'archive_year', info_dict),
   (r'^rss/latest/$', RssBlogFeed),
)
