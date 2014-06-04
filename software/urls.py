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
from software.views.list import SoftwareByTagView, SoftwareByAuthorView, SoftwareByLicenseView
from software.views.list import SoftwareByLanguageView, SoftwareByOpSysView, SoftwareByDataFormatView
from software.views.entry import AuthorsView, UsersView
from software.views.entry import TagsView, LicensesView, LanguagesView, OpSysView, DataFormatView
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
    (r'^author/$', AuthorsView.as_view()),
    (r'^author/(?P<slug>[^/]+)/$', SoftwareByAuthorView.as_view()),
    (r'^users/$', UsersView.as_view()),
    (r'^users/(?P<username>[^/]+)/$', SoftwareByUserView.as_view()),
    (r'^license/$', LicensesView.as_view()),
    (r'^license/(?P<slug>[^/]+)/$', SoftwareByLicenseView.as_view()),
    (r'^language/$', LanguagesView.as_view()),
    (r'^language/(?P<slug>[^/]+)/$', SoftwareByLanguageView.as_view()),
    (r'^search/$', 'software.forms.search_software'),
    (r'^rate/(?P<software_id>\d+)/$', 'software.views.entry.rate'),
    (r'^tags/$', TagsView.as_view()),
    (r'^tags/(?P<slug>[^/]+)/$', SoftwareByTagView.as_view()),
    (r'^opsys/$', OpSysView.as_view()),
    (r'^opsys/(?P<slug>[^/]+)/$', SoftwareByOpSysView.as_view()),
    (r'^dataformat/$', DataFormatView.as_view()),
    (r'^dataformat/(?P<slug>[^/]+)/$', SoftwareByDataFormatView.as_view()),
    (r'^forum/$', ListView.as_view(), forum_dict),
    (r'^mail/(?P<software_id>\d+)/$', 'software.forms.contact_author'), 
)
