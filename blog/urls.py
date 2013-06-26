from django.conf.urls import patterns
from blog.models import BlogItem
from blog.feeds import RssBlogFeed
from community.summary import get_latest_news
from django.views.generic.dates import YearArchiveView, MonthArchiveView, DayArchiveView
from django.views.generic.dates import DateDetailView
from django.views.generic.list import ListView

info_dict = {
    'queryset' : BlogItem.objects.all(),
    'date_field' : 'pub_date',
    'extra_context' : get_latest_news()
}


urlpatterns = patterns(
   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[A-Za-z0-9-_]+)/$', 
    DateDetailView.as_view(slug_field='slug')),
   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', DayArchiveView.as_view()),
   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', MonthArchiveView.as_view()),
   (r'^(?P<year>\d{4})/$', YearArchiveView.as_view, info_dict),
   (r'^rss/latest/$', RssBlogFeed),
)
