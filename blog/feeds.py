from wfwfeed import WellFormedWebRss
from blog.models import BlogItem
from django.contrib.sites.models import Site
from django.http import HttpResponse
from markdown import markdown

from community.summary import get_latest_news
from django.views.generic.list import ListView
from django.views.generic.dates import YearArchiveView
from django.views.generic.dates import MonthArchiveView
from django.views.generic.dates import DateDetailView


class BlogView(ListView):
    context_object_name='latest'

    def get_template_names(self):
        return 'community/blog_list.html'

    def get_queryset(self, **kwargs):
        return BlogItem.objects.all()
    
    def get_context_data(self, **kwargs):
        context=super(BlogView, self).get_context_data(**kwargs)
        context.update(get_latest_news())
	return context

class DetailView(DateDetailView):
    queryset=BlogItem.objects.all()
    date_field = "pub_date"

    def get_context_data(self, **kwargs):
        context=super(DetailView, self).get_context_data(**kwargs)
        context.update(get_latest_news())
        return context

class YearView(YearArchiveView):
    queryset=BlogItem.objects.all()
    date_field = "pub_date"

    def get_context_data(self, **kwargs):
        context=super(YearView, self).get_context_data(**kwargs)
        context.update(get_latest_news())
        return context

class MonthView(MonthArchiveView):
    queryset=BlogItem.objects.all()
    date_field = "pub_date"

    def get_context_data(self, **kwargs):
        context=super(MonthView, self).get_context_data(**kwargs)
        context.update(get_latest_news())
        return context

def RssBlogFeed(request):
    try:
        object_list = BlogItem.objects.all().order_by('-pub_date')[:10]
    except documents.DocumentDoesNotExist:
        raise Http404
    feed = WellFormedWebRss( u"The mloss.org community blog",
            "http://mloss.org/community",
            u'Some thoughts about machine learning open source software',
            language=u"en")

    for object in object_list:
        link = 'http://%s%s' % (Site.objects.get_current().domain, object.get_absolute_url())
        #commentlink=u'http://%s/software/rss/comments/%i' % (Site.objects.get_current().domain, object.id)
        #comments=commentlink,
        feed.add_item( object.headline.encode('utf-8'),
                link, markdown(object.body),
                author_name=object.author.encode('utf-8'),
                pubdate=object.pub_date, unique_id=link)
    response = HttpResponse(mimetype='application/xml')
    feed.write(response, 'utf-8')
    return response
