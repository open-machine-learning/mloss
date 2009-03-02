from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.comments.models import Comment
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from software.models import Software
from revision.models import Revision
from wfwfeed import WellFormedWebRss
from markdown import markdown

def RssSoftwareFeed(request):
    try:
        object_list = Revision.objects.filter(revision=0).order_by('-updated_date')[:10]
    except documents.DocumentDoesNotExist:
        raise Http404
    feed = WellFormedWebRss( u"mloss.org new software",
            "http://mloss.org",
            u'Updates and additions to mloss.org',
            language=u"en")

    for object in object_list:
        link = 'http://%s%s' % (Site.objects.get_current().domain, object.get_absolute_url())
        commentlink=u'http://%s/software/rss/comments/%i' % (Site.objects.get_current().domain, object.id)
        feed.add_item( object.software.title.encode('utf-8') + u' ' + object.version.encode('utf-8'),
                link, object.get_description_page(),
                author_name=object.authors.encode('utf-8'),
                comments=commentlink,
                pubdate=object.updated_date, unique_id=link,
                categories=[x.name for x in object.get_taglist()] )
    response = HttpResponse(mimetype='application/xml')
    feed.write(response, 'utf-8')
    return response

def RssSoftwareAndCommentsFeed(request, software_id):
    sw = get_object_or_404(Software, pk=software_id)
    ctype = ContentType.objects.get_for_model(sw)
    object_list = Comment.objects.filter(content_type=ctype, object_pk=sw.pk).order_by('submit_date')

    feed = WellFormedWebRss( u'mloss.org ' + sw.title.encode('utf-8'),
            "http://mloss.org",
            u'Updates and additions to ' + sw.title.encode('utf-8'),
            language=u"en")

    rev = get_object_or_404(Revision, software=sw, revision=0)
    link = 'http://%s%s' % (Site.objects.get_current().domain, sw.get_absolute_url())
    commentlink=u'http://%s/software/rss/comments/%i' % (Site.objects.get_current().domain, sw.id)
    feed.add_item( sw.title.encode('utf-8') + u' ' + rev.version.encode('utf-8'),
        link, rev.get_description_page(),
        author_name=rev.authors.encode('utf-8'),
        comments=commentlink,
        pubdate=rev.updated_date, unique_id=link,
        categories=[x.name for x in rev.get_taglist()] )

    for object in object_list:
        link = 'http://%s%s' % (Site.objects.get_current().domain, object.get_absolute_url())
        feed.add_item(u'<b>Comment by %s on %s</b>' % (object.name, object.submit_date.strftime("%Y-%m-%d %H:%M")),
                link, markdown(object.comment),
                author_name=object.name,
                pubdate=object.submit_date, unique_id=link,)
    response = HttpResponse(mimetype='application/xml')
    feed.write(response, 'utf-8')
    return response

def RssCommentsFeed(request, software_id):
    sw = get_object_or_404(Software, pk=software_id)
    ctype = ContentType.objects.get_for_model(sw)
    object_list = Comment.objects.filter(content_type=ctype, object_pk=sw.pk).order_by('submit_date')

    feed = WellFormedWebRss( u'mloss.org ' + sw.title.encode('utf-8'),
            "http://mloss.org",
            u'Updates and additions to ' + sw.title.encode('utf-8'),
            language=u"en")

    for object in object_list:
        link = 'http://%s%s' % (Site.objects.get_current().domain, object.get_absolute_url())
        feed.add_item(u'<b>By: %s on: %s</b>' % (object.name, object.submit_date.strftime("%Y-%m-%d %H:%M")),
                link, markdown(object.comment),
                author_name=object.name,
                pubdate=object.submit_date, unique_id=link,)
    response = HttpResponse(mimetype='application/xml')
    feed.write(response, 'utf-8')
    return response
