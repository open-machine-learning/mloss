"""
URLConf for Django-Forum.

django-forum assumes that the forum application is living under
/forum/.

Usage in your base urls.py:
	(r'^forum/', include('community.urls')),
"""

from django.conf.urls import url, include

from blog.feeds import BlogView

urlpatterns = [
	url(r'^$', BlogView.as_view()),
	url(r'^blog/', include('blog.urls')),
]
