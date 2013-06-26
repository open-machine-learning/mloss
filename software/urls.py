"""
URLConf for software.

Recommended usage is to use a call to ``include("software.urls")`` in your project's
root URLConf to include this URLConf for any URL beginning with
'/browse/'.

"""

from django.conf.urls import patterns
from django.views.generic.list import ListView
from software.views.list import SoftwareInJMLRView, SoftwareByUpdatedDateView
from software.views.list import SoftwareByUserView, SoftwareByPubdateView
from software.views.list import SoftwareByTitleView, SoftwareByRatingView
from software.views.list import SoftwareByViewsView, SoftwareByDownloadsView
from django.views.generic.detail import DetailView
from revision.models import Revision


from community.models import Forum
forum_dict = {
    'queryset' : Forum.objects.all(),
}


# General softwares views.
urlpatterns = patterns('',
    (r'^$', SoftwareByUpdatedDateView.as_view()),
    (r'^date/$', SoftwareByUpdatedDateView.as_view()),
    (r'^pubdate/$', SoftwareByPubdateView.as_view()),
    (r'^title/$', SoftwareByTitleView.as_view()),
    (r'^jmlr/$', SoftwareInJMLRView.as_view()),
    (r'^views/$', SoftwareByViewsView.as_view()),
    (r'^downloads/$', SoftwareByDownloadsView.as_view()),
    (r'^rating/$', SoftwareByRatingView.as_view()),
    (r'^view/(?P<software_id>\d+)/$', 'software.views.entry.software_detail'), 
    (r'^viewstats/(?P<software_id>\d+)/$', 'software.views.entry.viewstats'),
    (r'^downloadstats/(?P<software_id>\d+)/$', 'software.views.entry.downloadstats'),
    (r'^viewstatspreview/(?P<software_id>\d+)/$', 'software.views.entry.viewstatspreview'),
    (r'^downloadstatspreview/(?P<software_id>\d+)/$', 'software.views.entry.downloadstatspreview'),
    (r'^submit/', 'software.forms.add_software'),
    (r'^update/(?P<software_id>\d+)/$', 'software.forms.edit_software'),
    (r'^update/(?P<software_id>\d+)/(?P<revision_id>\d+)$', 'software.forms.edit_software'),
    (r'^subscribe/(?P<software_id>\d+)/$', 'software.views.entry.subscribe_software'),
    (r'^bookmark/(?P<software_id>\d+)/$', 'software.views.entry.bookmark_software'),
    (r'^rmbookmark/(?P<software_id>\d+)/$', 'software.views.entry.remove_bookmark'),
    (r'^unsubscribe/(?P<software_id>\d+)/$', 'software.views.entry.unsubscribe_software'),
    (r'^rss/latest/$', 'software.feeds.RssSoftwareFeed'),
    (r'^rss/merged/(?P<software_id>\d+)/$', 'software.feeds.RssSoftwareAndCommentsFeed'),
    (r'^rss/comments/(?P<software_id>\d+)/$', 'software.feeds.RssCommentsFeed'),
    (r'^author/$', 'software.views.entry.software_all_authors'),
    (r'^author/(?P<slug>[^/]+)/$', 'software.views.list.software_by_author'),
    (r'^users/$', 'software.views.entry.user_with_software'),
    (r'^users/(?P<username>[^/]+)/$', SoftwareByUserView.as_view()),
    (r'^license/$', 'software.views.entry.software_all_licenses'),
    (r'^license/(?P<slug>[^/]+)/$', 'software.views.list.software_by_license'),
    (r'^language/$', 'software.views.entry.software_all_languages'),
    (r'^language/(?P<slug>[^/]+)/$', 'software.views.list.software_by_language'),
    (r'^search/$', 'software.forms.search_software'),
    (r'^rate/(?P<software_id>\d+)/$', 'software.views.entry.rate'),
    (r'^tags/$', 'software.views.entry.software_all_tags'),
    (r'^tags/(?P<slug>[^/]+)/$', 'software.views.list.software_by_tag'),
    (r'^opsys/$', 'software.views.entry.software_all_opsyss'),
    (r'^opsys/(?P<slug>[^/]+)/$', 'software.views.list.software_by_opsys'),
    (r'^dataformat/$', 'software.views.entry.software_all_dataformats'),
    (r'^dataformat/(?P<slug>[^/]+)/$', 'software.views.list.software_by_dataformats'),
    (r'^forum/$', 'ListView.as_view', forum_dict),
    (r'^mail/(?P<software_id>\d+)/$', 'software.forms.contact_author'), 
)
