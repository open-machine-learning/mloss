from wfwfeed import WellFormedWebRss
from blog.models import BlogItem
from django.contrib.sites.models import Site
from django.http import HttpResponse
from markdown import markdown

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
