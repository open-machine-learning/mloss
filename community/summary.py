from community.models import Forum,Thread,Post
from django.template import RequestContext
from aggregator.models import Feed, FeedItem
from blog.models import BlogItem

class ForumSummary():
	"""
	Summarises latest forum posts
	"""
	title = ''
	url = ''
	body = ''
	author = ''
	time = ''
	thread = ''

class FeedSummary():
	"""
	Summarises the latest feeds from external sites
	"""
	title = ''
	url = ''
	items = []


def get_latest_posts():
	"""
	For each Forum, get the latest post
	"""
	latest_posts = []
	all_forums = Forum.objects.all()
	for forum in all_forums:
		summary = ForumSummary()
		summary.title = forum.title
		post = forum.forum_latest_post
		if post:
			summary.body = post.body
			summary.url = post.get_absolute_url()
			summary.author = post.author
			summary.pub_date = post.time
		if post.thread:
			summary.thread = post.thread.title
		latest_posts.append(summary)
	return latest_posts

def get_latest_feeds():
	"""
	For each feed from an external site, get the latest post title
	"""
	all_feeds = Feed.objects.all()

	latest_feeds = []
	for feed in all_feeds:
		cur_feed = FeedSummary()
		cur_feed.title = feed.title
		cur_feed.url = feed.public_url
		items = FeedItem.objects.filter(feed__title=feed.title).order_by('-date_modified')
		cur_feed.items = items[:3]

		latest_feeds.append(cur_feed)

	return latest_feeds

def get_latest_news(extra=None):
	if extra is None:
		extra=dict()

	latest_posts = get_latest_posts()
	latest_feeds = get_latest_feeds()
	blog_entries = BlogItem.objects.order_by('-pub_date')[:10]
	extra['latest_posts']=latest_posts
	extra['latest_feeds']=latest_feeds
	extra['blog_entries']=blog_entries
	extra['blog_years']=BlogItem.objects.dates('pub_date', 'year')
	return extra
