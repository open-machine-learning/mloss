from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed
from software.models import Software
from django.utils.feedgenerator import Atom1Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.http import HttpResponse
from django.http import Http404

def RssSoftwareFeed(request):
    try:
        object_list = Software.objects.all().order_by('-pub_date')[:10]
    except documents.DocumentDoesNotExist:
        raise Http404
    feed = Rss201rev2Feed( u"mloss.org new software",
            "http://mloss.org",
            u'Updates and additions to mloss.org',
            language=u"en")

    for object in object_list:
        link = 'http://%s%s' % (Site.objects.get_current().domain, object.get_absolute_url())
        feed.add_item( object.title.encode('utf-8'),
                link, object.get_description_page(),
                author_name=object.authors.encode('utf-8'),
                pubdate=object.pub_date, unique_id=link,
                categories=[x.name for x in object.get_taglist()] )
    response = HttpResponse(mimetype='application/xml')
    feed.write(response, 'utf-8')
    return response
