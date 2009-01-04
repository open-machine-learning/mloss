"""
URLConf for software.

Recommended usage is to use a call to ``include("software.urls")`` in your project's
root URLConf to include this URLConf for any URL beginning with
'/browse/'.

"""

from django.conf.urls.defaults import *

from community.models import Forum
forum_dict = {
    'queryset' : Forum.objects.all(),
}


# General softwares views.
urlpatterns = patterns('',
    (r'^view/(?P<software_id>\d+)/$', 'software.views.entry.software_detail'), 
    (r'^$', 'software.views.list.software_by_updated_date'),
    (r'^date/$', 'software.views.list.software_by_updated_date'),
    (r'^pubdate/$', 'software.views.list.software_by_pub_date'),
    (r'^title/$', 'software.views.list.software_by_title'),
    (r'^jmlr/$', 'software.views.list.software_in_jmlr'),
    (r'^views/$', 'software.views.list.software_by_views'),
    (r'^viewstats/(?P<software_id>\d+)/$', 'software.views.entry.viewstats'),
    (r'^downloadstats/(?P<software_id>\d+)/$', 'software.views.entry.downloadstats'),
    (r'^viewstatspreview/(?P<software_id>\d+)/$', 'software.views.entry.viewstatspreview'),
    (r'^downloadstatspreview/(?P<software_id>\d+)/$', 'software.views.entry.downloadstatspreview'),
    (r'^downloads/$', 'software.views.list.software_by_downloads'),
    (r'^rating/$', 'software.views.list.software_by_rating'),
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
    (r'^users/(?P<username>[^/]+)/$', 'software.views.list.software_by_user'),
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
    (r'^forum/$', 'django.views.generic.list_detail.object_list', forum_dict),
    (r'^mail/(?P<software_id>\d+)/$', 'software.forms.contact_author'), 
)
