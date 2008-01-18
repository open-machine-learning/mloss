from django.shortcuts import get_object_or_404
from django.contrib.sites.models import Site
from django.http import HttpResponse, Http404
from django.utils.xmlutils import SimplerXMLGenerator
from community.models import Forum,Thread,Post
from markdown import markdown
from wfwfeed import WellFormedWebRss

def ForumFeed(request, forum):
    f = get_object_or_404(Forum, slug=forum)
    try:
        object_list = f.thread_set.all()
    except documents.DocumentDoesNotExist:
        raise Http404
    feed = WellFormedWebRss( u"mloss.org community forum %s" % f.title.encode('utf-8'),
            "http://mloss.org",
            u'Updates to mloss.org forum %s' % f.title.encode('utf-8'),
            language=u"en")

    for thread in object_list:
        link = u'http://%s%s' % (Site.objects.get_current().domain, thread.get_absolute_url())
        commentlink=u'http://%s%s' % (Site.objects.get_current().domain, thread.get_absolute_url())
        commentrss=u'http://%s/community/rss/thread/%i' % (Site.objects.get_current().domain, thread.id)
        feed.add_item( thread.title.encode('utf-8'),
                commentlink, None,
                comments=commentlink,
                pubdate=thread.thread_latest_post.time, unique_id=link)
        feed.add_commentRss(commentrss)

    response = HttpResponse(mimetype='application/xml')
    feed.write(response, 'utf-8')
    return response

def ThreadFeed(request, forum, thread):
    thread = get_object_or_404(Thread, pk=thread)

    feed = WellFormedWebRss( u"mloss.org community forum",
            "http://mloss.org",
            u'Updates to mloss.org thread %s' % thread.title.encode('utf-8'),
            language=u"en")

    for post in thread.post_set.all().order_by('time'):
            link = u'http://%s%s' % (Site.objects.get_current().domain, post.get_absolute_url())
            feed.add_item(u'<b>By: %s on: %s</b>' % (post.author.username, post.time.strftime("%Y-%m-%d %H:%M")),
                    link, markdown(post.body), 
                    author_name=post.author.username,
                    pubdate=post.time, unique_id=link)

    response = HttpResponse(mimetype='application/xml')
    feed.write(response, 'utf-8')
    return response
