""" 
A basic forum model with corresponding thread/post models.

Just about all logic required for smooth updates is in the save() 
methods. A little extra logic is in views.py.
"""

from django.db import models
import datetime
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from mloss.subscriptions.models import Subscriptions
from utils import send_mails

class Forum(models.Model):
	"""
	Very basic outline for a Forum, or group of threads. The threads
	and posts fielsd are updated by the save() methods of their
	respective models and are used for display purposes.
	"""
	title = models.CharField(max_length=100)
	slug = models.SlugField()
	description = models.TextField()
	threads = models.IntegerField(default=0)
	posts = models.IntegerField(default=0)
	forum_latest_post = models.ForeignKey('Post', blank=True, null=True, related_name='forum_latest_post')

	def get_absolute_url(self):
		return '/community/%s/' % self.slug

	def __unicode__(self):
		return unicode(self.title)

	def subscribe(self, user, bookmark):
		ctype = ContentType.objects.get_for_model(self)
		Subscriptions.objects.get_or_create(title="Forum " + self.title,
				content_type=ctype, object_id=self.id, user=user,
				url=self.get_absolute_url(), bookmark=bookmark)

	def unsubscribe(self, user, bookmark):
		ctype = ContentType.objects.get_for_model(self)
		object=get_object_or_404(Subscriptions, content_type=ctype, object_id=self.id,
				user=user, bookmark=bookmark)
		object.delete()

	def save(self):
		super(Forum, self).save()

	def notify_update(self):
		ctype = ContentType.objects.get_for_model(self)
		subscribers=Subscriptions.objects.filter(content_type=ctype, object_id=self.id)

		subject='Updates on mloss.org community forum ' + self.title
		message='''Dear mloss.org user,

you are receiving this email as you have subscribed to the "'''

		message+=self.title
		message+='''" community forum,
which has just been updated.

Feel free to visit mloss.org to see what has changed.

		'''
		message+='http://%s%s' % (Site.objects.get_current().domain, self.get_absolute_url())
		message+='''

Friendly,
   your mloss.org team.
        '''

		send_mails(subscribers, subject, message)

class Thread(models.Model):
	"""
	A Thread belongs in a Forum, and is a collection of posts.

	Threads can be closed or stickied which alter their behaviour 
	in the thread listings. Again, the posts & views fields are 
	automatically updated with saving a post or viewing the thread.
	"""
	forum = models.ForeignKey(Forum)
	title = models.CharField(max_length=100)
	sticky = models.BooleanField(blank=True, null=True)
	closed = models.BooleanField(blank=True, null=True)
	posts = models.IntegerField(default=0)
	views = models.IntegerField(default=0)
	thread_latest_post = models.ForeignKey('Post', blank=True, null=True, related_name='thread_latest_post')

	class Meta:
		ordering = ('-sticky', '-thread_latest_post')

	def save(self):
		if not self.id:
			f = Forum.objects.get(id=self.forum.id)
			f.threads += 1
			f.save()
		super(Thread, self).save()
	
	def get_absolute_url(self):
		return '/community/%s/%s/' % (self.forum.slug, self.id)
	
	def __unicode__(self):
		return unicode(self.title)

	def subscribe(self, user, bookmark):
		ctype = ContentType.objects.get_for_model(self)
		Subscriptions.objects.get_or_create(title="Thread " + self.title,
				content_type=ctype, object_id=self.id, user=user,
				url=self.get_absolute_url(), bookmark=bookmark)

	def unsubscribe(self, user, bookmark):
		ctype = ContentType.objects.get_for_model(self)
		object=get_object_or_404(Subscriptions, content_type=ctype, object_id=self.id,
				user=user, bookmark=bookmark)
		object.delete()

	def notify_update(self):
		ctype = ContentType.objects.get_for_model(self)
		subscribers=Subscriptions.objects.filter(content_type=ctype, object_id=self.id)

		subject='Updates on mloss.org community thread ' + self.title
		message='''Dear mloss.org user,

you are receiving this email as you have subscribed to the "'''

		message+=self.title
		message+='''" community thread,
which has just been updated.

Feel free to visit mloss.org to see what has changed.
    
        '''
		message+='http://%s%s' % (Site.objects.get_current().domain, self.get_absolute_url())
		message+='''

Friendly,
   your mloss.org team.
        '''

		send_mails(subscribers, subject, message)

class Post(models.Model):
	""" 
	A Post is a User's input to a thread. Uber-basic - the save() 
	method also updates models further up the heirarchy (Thread,Forum)
	"""
	thread = models.ForeignKey(Thread)
	author = models.ForeignKey(User)
	body = models.TextField()
	time = models.DateTimeField(blank=True, null=True)

	def save(self):
		new_post = False
		if not self.id:
			self.time = datetime.datetime.now()
			new_post = True
			
		super(Post, self).save()

		if new_post:
			t=self.thread
			t.thread_latest_post_id = self.id
			t.posts += 1
			t.save()
			t.notify_update()

			f = self.thread.forum
			f.forum_latest_post_id = self.id
			f.posts += 1
			f.save()
			f.notify_update()

	class Meta:
		ordering = ('-time',)
		
	def get_absolute_url(self):
		p=0
		for t in Post.objects.filter(thread=self.thread):
			if t.id == self.id:
				return '/community/%s/%s/?page=%d#post%s' % (self.thread.forum.slug, self.thread.id, p / 10+1, self.id)
			p+=1
	
	def __unicode__(self):
		return u"%s" % self.id
