"""
All forum logic is kept here - displaying lists of forums, threads 
and posts, adding new threads, and adding replies.
"""

from community.models import Forum,Thread,Post
from community.models import Forum
from datetime import datetime
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django import forms
from django.contrib.auth import authenticate, login

from django.views.generic.list import ListView
from community.summary import get_latest_news

class NewPostForm(forms.Form):
	body = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":80}))

class NewPostFormwPassword(forms.Form):
	password = forms.CharField(widget=forms.PasswordInput(attrs={'size':'20'}), required=True, max_length=40)
	username = forms.CharField(widget=forms.TextInput(attrs={'size':'20'}), required=True, max_length=40)
	body = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":80}))

	def clean_username(self):
		if 'username' not in self.cleaned_data:
			raise forms.ValidationError(u'This field is required.')
		if 'username' in self.cleaned_data and 'password' in self.cleaned_data:
			try:
				username=self.cleaned_data['username']
				password=self.cleaned_data['password']
				username=username.decode()
				password=password.decode()
			except:
				raise forms.ValidationError(u'Please enter a correct username and password. Note that both fields are case-sensitive.')
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					self.user = user
				else:
					raise forms.ValidationError(u'User Account disabled.')
			else:
				raise forms.ValidationError(u'Please enter a correct username and password. Note that both fields are case-sensitive.')

	def login(self, request):
		if self.is_valid():
			login(request, self.user)
			return request.user.is_authenticated()
		return False

def create_newpostform(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			inputform = NewPostForm(request.POST)
		else:
			inputform = NewPostForm()
	else:
		if request.method == 'POST':
			inputform = NewPostFormwPassword(request.POST)
		else:
			inputform = NewPostFormwPassword()
	return inputform

class NewThreadForm(forms.Form):
	body = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":80}))
	title = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}), required=True, max_length=100)

class NewThreadFormwPassword(forms.Form):
	password = forms.CharField(widget=forms.PasswordInput(attrs={'size':'20'}), required=True, max_length=40)
	username = forms.CharField(widget=forms.TextInput(attrs={'size':'20'}), required=True, max_length=40)
	title = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}), required=True, max_length=100)
	body = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":80}))

	def clean_username(self):
		if 'username' not in self.cleaned_data:
			raise forms.ValidationError(u'This field is required.')
		if 'username' in self.cleaned_data and 'password' in self.cleaned_data:
			username=self.cleaned_data['username']
			password=self.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					self.user = user
				else:
					raise forms.ValidationError(u'User Account disabled.')
			else:
				raise forms.ValidationError(u'Please enter a correct username and password. Note that both fields are case-sensitive.')

	def login(self, request):
		if self.is_valid():
			login(request, self.user)
			return True
		return False

def create_newthreadform(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			inputform = NewThreadForm(request.POST)
		else:
			inputform = NewThreadForm()
	else:
		if request.method == 'POST':
			inputform = NewThreadFormwPassword(request.POST)
		else:
			inputform = NewThreadFormwPassword()
	return inputform


def forum(request, slug):
 	"""
 	Displays a list of threads within a forum.
 	Threads are sorted by their sticky flag, followed by their 
 	most recent post.
 	"""
 	f = get_object_or_404(Forum, slug=slug)
 	inputform = create_newthreadform(request)
 	extra= get_latest_news()
 	extra['forum']=f
 	extra['form']=inputform
 	extra['form_action']='new/'
 	extra['threads']=f.thread_set.all().order_by('thread_latest_post')

 	return render(request, 'community/thread_list.html',
 		{'context':  extra})


class ForumView(ListView):

	def get_queryset(self, **kwargs):
		return Forum.objects.all()
	
	def get_context_data(self, **kwargs):
		return get_latest_news()


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

 	inputform = create_newpostform(request)
 	extra= get_latest_news()
 	extra['forum']=f
 	extra['form']=inputform
 	extra['thread']=t
 	extra['form_action']='reply/'

 	return ListView.as_view(request,
 			paginate_by=10,
 			queryset=p,
 			template_name='community/thread.html',
 			extra_context=extra)

def newthread(request, forum):
	"""
	Rudimentary post function.
        
	Only allows a user to post if they're logged in.
	"""
	f = get_object_or_404(Forum, slug=forum)
	t = f.thread_set.all().order_by('thread_latest_post')[:1]

	if request.method == 'POST':
		form = create_newthreadform(request)
		if form.is_valid():
			if request.user.is_authenticated() or form.login(request):
				t = Thread(
					forum=f,
					title=form.cleaned_data['title'],
				)
				if form.data.has_key(u'post'):
					t.save()
				p = Post(
					thread=t,
					author=request.user,
					body=form.cleaned_data['body'],
					time=datetime.now(),
				)
				if form.data.has_key(u'post'):
					p.save()
					return HttpResponseRedirect(t.get_absolute_url())
				else:
					return render(request, 'community/thread_list.html', {
							'posting' : p,
							'forum': f,
							'form': form,
							'form_action' : '',
							'thread': t
							})
	else:
		form = create_newthreadform(request)
	
	return render(request, 'community/thread_list.html', {
			'forum': f,
			'form': form,
			'form_action' : '',
			'threads': t
			})



class Reply(ListView):
	def get_template_names(self):
		return 'community/thread.html'

	def get_queryset(self, **kwargs):
		forum = self.kwargs['forum']
                thread = self.kwargs['thread']
		f = get_object_or_404(Forum, slug=forum)
		t = get_object_or_404(Thread, pk=thread)
		p = t.post_set.all().order_by('-time')[:1]

		if t.closed:
			return HttpResponseRedirect('/accounts/login?next=%s' % request.path)

		if request.method == 'POST':
			form = create_newpostform(request)

			if form.is_valid():
				if request.user.is_authenticated() or form.login(request):
					p = Post(
						thread=t, 
						author=request.user,
						body=form.cleaned_data['body'],
						time=datetime.now(),
						)
					if form.data.has_key(u'post'):
						p.save()
						return HttpResponseRedirect(p.get_absolute_url())
					else:
						return render(request, 'community/thread.html',{
								'forum': f,
								'form': form,
								'thread': t,
								'posting': p,
								'form_action' : ''})
		else:
			form = create_newpostform(request)
		return p
	
	def get_context_data(self, **kwargs):
		forum = self.kwargs['forum']
                thread = self.kwargs['thread']
                f = get_object_or_404(Forum, slug=forum)
                t = get_object_or_404(Thread, pk=thread)

		extra_context= {
			'forum': f,
			'form': form,
			'thread': t,
			'form_action' : ''}
		return extra_context
	
	def get_paginate_by(self):
		return 10


def community_base(request):
		return ListView.as_view(request,
					template_name='community_base.html',)


def get_summary_page(request):
	"""
	Get a summary of:
	- Latest forum posts
	- Latest feeds from external sites
	"""
	return render(request, 'community/summary.html',
			{'context': get_latest_news()})
