"""
URLConf for revision.

Recommended usage is to use a call to ``include("revision.urls")`` in your project's
root URLConf to include this URLConf for any URL beginning with
'/browse/'.

"""


from django.conf.urls import url, include

from revision.views import revision_detail
from revision.views import view_homepage
from revision.views import view_jmlr_homepage
from revision.views import download_revision
from revision.views import get_bibitem
from revision.views import get_paperbibitem


# General revision views.
urlpatterns = [
    url(r'^view/(?P<revision_id>\d+)/$', revision_detail, name='revision_detail'),
    url(r'^homepage/(?P<revision_id>\d+)/$', view_homepage, name='view_homepage'),
    url(r'^jmlrhomepage/(?P<revision_id>\d+)/$', view_jmlr_homepage, name='view_jmlr_homepage'),
    url(r'^download/(?P<revision_id>\d+)/$', download_revision, name='download_revision'),
    url(r'^bib/(?P<revision_id>\d+)/$', get_bibitem, name='get_bibitem'),
    url(r'^paperbib/(?P<revision_id>\d+)/$', get_paperbibitem, name='get_paperbibitem'),
]

