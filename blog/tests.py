import datetime
from django.test import TestCase
from django.contrib.auth.models import User

class BlogTest(TestCase):
    # local urls won't work, coz templates refer to repository_index
    #urls = 'user.urls'
    url = {
        'index': '/blog/',
        'new': '/blog/new/',
        'byyear': '/community/blog/2013/'
    }
    entry = {
        'headline':'headline',
        'summary':'summary',
        'body':'body',
    }
    date = {
        'year': '2010',
        'month': '03',
        'day': '30',
    }
    fixtures = ['test_data.json']


    def setUp(self):
        pass
#   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[A-Za-z0-9-_]+)/$', 
#    DateDetailView.as_view(slug_field='slug')),
#   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', DayArchiveView.as_view()),
#   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', MonthArchiveView.as_view()),
#   (r'^(?P<year>\d{4})/$', YearArchiveView.as_view, info_dict),
#   (r'^rss/latest/$', RssBlogFeed),


    def test_index(self):
        r = self.client.get(self.url['byyear'])
        self.assertTemplateUsed(r, 'blog/blogitem_archive_year.html')
