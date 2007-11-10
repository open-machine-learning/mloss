from django.shortcuts import get_object_or_404
from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed
from django.http import HttpResponse, Http404
from community.models import Forum,Thread,Post
from markdown import markdown

def RssFeed(request, forum):
    f = get_object_or_404(Forum, slug=forum)
    try:
        object_list = f.thread_set.all() #.order_by('-pub_date')[:10]
    except documents.DocumentDoesNotExist:
        raise Http404
    feed = Rss201rev2Feed( u"mloss.org community forum",
            "http://mloss.org",
            u'Updates to mloss.org forum %s' % f.title.encode('utf-8'),
            language=u"en")

    for thread in object_list:
        link = 'http://%s%s' % (Site.objects.get_current().domain, thread.get_absolute_url())
        posts_body=u''

        for post in thread.post_set.all().order_by('time'):
            posts_body+='<b>Author:</b>%s<br><b>Date:</b> %s' % ( post.author.username, post.time)
            posts_body+=markdown(post.body)
            posts_body+='<hr>'

        feed.add_item( thread.title.encode('utf-8'),
                link, posts_body,
                pubdate=thread.thread_latest_post.time, unique_id=link)
        response = HttpResponse(mimetype='application/xml')
    feed.write(response, 'utf-8')
    return response

#def RssFeed(request, forum):
#    f = get_object_or_404(Forum, slug=forum)
#    try:
#        object_list = f.thread_set.all() #.order_by('-pub_date')[:10]
#    except documents.DocumentDoesNotExist:
#        raise Http404
#    feed = Rss201rev2Feed( u"mloss.org community forum",
#            "http://mloss.org",
#            u'Updates to mloss.org forum %s' % f.title.encode('utf-8'),
#            language=u"en")
#
#    for thread in object_list:
#        for post in thread.post_set.all().order_by('-time')[:5]:
#            link = 'http://%s%s' % (Site.objects.get_current().domain, post.get_absolute_url())
#            feed.add_item( thread.title.encode('utf-8'),
#                    link, post.body,
#                    author_name=post.author.username.encode('utf-8'),
#                    pubdate=post.time, unique_id=link)
#            response = HttpResponse(mimetype='application/xml')
#    feed.write(response, 'utf-8')
#    return response
#
