"""
All forum logic is kept here - displaying lists of forums, threads 
and posts, adding new threads, and adding replies.
"""

from djangoforum.models import Forum,Thread,Post
from datetime import datetime
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext
from django import newforms as forms

def forum(request, slug):
	"""
	Displays a list of threads within a forum.
	Threads are sorted by their sticky flag, followed by their 
	most recent post.
	"""
	f = get_object_or_404(Forum, slug=slug)

	return render_to_response('djangoforum/thread_list.html',
		RequestContext(request, {
			'forum': f,
			'threads': f.thread_set.all()
		}))

def thread(request, forum, thread):
	"""
	Increments the viewed count on a thread then displays the 
	posts for that thread, in chronological order.
	"""
	f = get_object_or_404(Forum, slug=forum)
	t = get_object_or_404(Thread, pk=thread)
	p = t.post_set.all().order_by('time')

	t.views += 1
	t.save()
	
	return render_to_response('djangoforum/thread.html',
		RequestContext(request, {
			'forum': f,
			'thread': t,
			'posts': p,
		}))

def reply(request, forum, thread):
	"""
	If a thread isn't closed, and the user is logged in, post a reply
	to a thread. Note we don't have "nested" replies at this stage.
	"""
	if not request.user.is_authenticated:
		raise HttpResponseServerError
	f = get_object_or_404(Forum, slug=forum)
	t = get_object_or_404(Thread, pk=thread)
	if t.closed:
		raise HttpResponseServerError
	body = request.POST.get('body', False)
	p = Post(
		thread=t, 
		author=request.user,
		body=body,
		time=datetime.now(),
		)
	p.save()
	return HttpResponseRedirect(p.get_absolute_url())

def newthread(request, forum):
	"""
	Rudimentary post function - this should probably use 
	newforms, although not sure how that goes when we're updating 
	two models.

	Only allows a user to post if they're logged in.
	"""
	if not request.user.is_authenticated:
		raise HttpResponseServerError
	f = get_object_or_404(Forum, slug=forum)
	t = Thread(
		forum=f,
		title=request.POST.get('title'),
	)
	t.save()
	p = Post(
		thread=t,
		author=request.user,
		body=request.POST.get('body'),
		time=datetime.now(),
	)
	p.save()
	return HttpResponseRedirect(t.get_absolute_url())
