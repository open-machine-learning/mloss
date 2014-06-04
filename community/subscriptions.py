from django.shortcuts import get_object_or_404
from django.contrib.sites.models import Site
from django.http import HttpResponse, HttpResponseRedirect, Http404
from community.models import Forum,Thread,Post

def SubscribeForum(request, forum, bookmark=False):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login?next=%s' % request.path)
    entry = get_object_or_404(Forum, slug=forum)
    entry.subscribe(request.user, bookmark)
    return HttpResponseRedirect("/user/view/" + str(request.user.id) + "/")

def UnsubscribeForum(request, forum, bookmark=False):
    if not request.user.is_authenticated():
       return HttpResponseRedirect('/accounts/login?next=%s' % request.path)
    entry = get_object_or_404(Forum, slug=forum)
    entry.unsubscribe(request.user, bookmark)

    return HttpResponseRedirect("/user/view/" + str(request.user.id) + "/")

def BookmarkForum(request, forum):
    return SubscribeForum(request, forum, bookmark=True)
def RemoveBookmarkForum(request, forum):
    return UnsubscribeForum(request, forum, bookmark=True)

def SubscribeThread(request, forum, thread, bookmark=False):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login?next=%s' % request.path)
    entry = get_object_or_404(Thread, pk=thread)
    entry.subscribe(request.user, bookmark)
    return HttpResponseRedirect("/user/view/" + str(request.user.id) + "/")

def BookmarkThread(request, forum, thread):
    return SubscribeThread(request, forum, thread, bookmark=True)

def UnsubscribeThread(request, forum, thread, bookmark=False):
    if not request.user.is_authenticated():
       return HttpResponseRedirect('/accounts/login?next=%s' % request.path)
    entry = get_object_or_404(Thread, pk=thread)
    entry.unsubscribe(request.user, bookmark)

    return HttpResponseRedirect("/user/view/" + str(request.user.id) + "/")

def RemoveBookmarkThread(request, forum, thread):
    return UnsubscribeThread(request, forum, thread, bookmark=True)
