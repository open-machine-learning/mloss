"""
URLConf for software.

Recommended usage is to use a call to ``include("software.urls")`` in your project's
root URLConf to include this URLConf for any URL beginning with
'/browse/'.

"""

from django.conf.urls import url, include

from software.views.list import SoftwareByUpdatedDate
from software.views.list import SoftwareByAuthor
from software.views.list import SoftwareByTag
from software.views.list import SoftwareByLicense
from software.views.list import SoftwareByLanguage
from software.views.list import SoftwareByOpSys
from software.views.list import SoftwareByDataFormats
from software.views.list import SoftwareByPubDate
from software.views.list import SoftwareByTitle
from software.views.list import SoftwareBySubscription
from software.views.list import SoftwareByRating
from software.views.list import SoftwareByDownloads
from software.views.list import SoftwareByViews
from software.views.list import SoftwareInJmlr
from software.views.list import SoftwareByUser

from software.views.entry import SoftwareAllAuthors
from software.views.entry import SoftwareAllDataFormats
from software.views.entry import SoftwareAllLanguages
from software.views.entry import SoftwareAllLicenses
from software.views.entry import SoftwareAllOpSyss
from software.views.entry import SoftwareAllTags
from software.views.entry import UserWithSoftware
from software.views.entry import subscribe_software
from software.views.entry import unsubscribe_software
from software.views.entry import remove_bookmark
from software.views.entry import bookmark_software
from software.views.entry import software_detail
#from software.views.entry import viewstats
#from software.views.entry import downloadstats
#from software.views.entry import viewstatspreview
#from software.views.entry import downloadstatspreview
from software.views.entry import rate
from software.views.entry import SoftwareDetail

from software.feeds import RssSoftwareFeed
from software.feeds import RssCommentsFeed
from software.feeds import RssSoftwareAndCommentsFeed

from software.forms import add_software
from software.forms import edit_software
from software.forms import search_software
from software.forms import contact_author

from software.views.list import ForumClassView


from community.models import Forum


# General softwares views.
urlpatterns = [
    url(r'^view/(?P<software_id>\d+)/$', software_detail, name="sw_detail"), 
    url(r'^disp/(?P<software_id>\d+)/$', SoftwareDetail.as_view()), 
    url(r'^$',  SoftwareByUpdatedDate.as_view()),
    url(r'^date/$', SoftwareByUpdatedDate.as_view()),
    url(r'^pubdate/$', SoftwareByPubDate.as_view()),
    url(r'^title/$', SoftwareByTitle.as_view()),
    url(r'^jmlr/$', SoftwareInJmlr.as_view()),
    url(r'^views/$', SoftwareByViews.as_view()),
    #url(r'^viewstats/(?P<software_id>\d+)/$', viewstats),
    #url(r'^downloadstats/(?P<software_id>\d+)/$', downloadstats),
    #url(r'^viewstatspreview/(?P<software_id>\d+)/$', viewstatspreview),
    #url(r'^downloadstatspreview/(?P<software_id>\d+)/$', downloadstatspreview),
    url(r'^downloads/$', SoftwareByDownloads.as_view()),
    url(r'^rating/$', SoftwareByRating.as_view()),
    url(r'^submit/', add_software),
    url(r'^update/(?P<software_id>\d+)/$', edit_software),
    url(r'^update/(?P<software_id>\d+)/(?P<revision_id>\d+)$', edit_software),
    url(r'^subscribe/(?P<software_id>\d+)/$', subscribe_software),
    url(r'^bookmark/(?P<software_id>\d+)/$', bookmark_software),
    url(r'^rmbookmark/(?P<software_id>\d+)/$', remove_bookmark),
    url(r'^unsubscribe/(?P<software_id>\d+)/$', unsubscribe_software),
    url(r'^rss/latest/$', RssSoftwareFeed),
    url(r'^rss/merged/(?P<software_id>\d+)/$', RssSoftwareAndCommentsFeed),
    url(r'^rss/comments/(?P<software_id>\d+)/$', RssCommentsFeed),
    url(r'^author/$', SoftwareAllAuthors.as_view()),
    url(r'^author/(?P<slug>[^/]+)/$', SoftwareByAuthor.as_view(), name="sw_by_author"),
    url(r'^users/$', UserWithSoftware.as_view()),
    url(r'^users/(?P<username>[^/]+)/$', SoftwareByUser.as_view()),
    url(r'^license/$', SoftwareAllLicenses.as_view()),
    url(r'^license/(?P<slug>[^/]+)/$', SoftwareByLicense.as_view(), name="sw_by_license"),
    url(r'^language/$', SoftwareAllLanguages.as_view()),
    url(r'^language/(?P<slug>[^/]+)/$', SoftwareByLanguage.as_view(), name="sw_by_language"),
    url(r'^search/$', search_software),
    url(r'^rate/(?P<software_id>\d+)/$', rate),
    url(r'^tags/$', SoftwareAllTags.as_view()),
    url(r'^tags/(?P<slug>[^/]+)/$', SoftwareByTag.as_view(), name="sw_by_tag"),
    url(r'^opsys/$', SoftwareAllOpSyss.as_view()),
    url(r'^opsys/(?P<slug>[^/]+)/$', SoftwareByOpSys.as_view(), name="sw_by_opsys"),
    url(r'^dataformat/$', SoftwareAllDataFormats.as_view()),
    url(r'^dataformat/(?P<slug>[^/]+)/$', SoftwareByDataFormats.as_view(), name="sw_by_dataformat"),
    url(r'^forum/$', ForumClassView.as_view()),
    url(r'^mail/(?P<software_id>\d+)/$', contact_author), 
]
