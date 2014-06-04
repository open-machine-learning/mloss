"""
URLConf for revision.

Recommended usage is to use a call to ``include("revision.urls")`` in your project's
root URLConf to include this URLConf for any URL beginning with
'/browse/'.

"""

from django.conf.urls import patterns


# General revision views.
urlpatterns = patterns('',
    (r'^view/(?P<revision_id>\d+)/$', 'revision.views.revision_detail'),
    (r'^homepage/(?P<revision_id>\d+)/$', 'revision.views.view_homepage'),
    (r'^jmlrhomepage/(?P<revision_id>\d+)/$', 'revision.views.view_jmlr_homepage'),
    (r'^download/(?P<revision_id>\d+)/$', 'revision.views.download_revision'),
    (r'^bib/(?P<revision_id>\d+)/$', 'revision.views.get_bibitem'),
    (r'^paperbib/(?P<revision_id>\d+)/$', 'revision.views.get_paperbibitem'),
)

