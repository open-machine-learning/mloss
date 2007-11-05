"""
URLConf for software.

Recommended usage is to use a call to ``include("software.urls")`` in your project's
root URLConf to include this URLConf for any URL beginning with
'/browse/'.

"""

from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list
from models import Software
from views.entry import software_detail
from software.feeds import RssSoftwareFeed

# Info for generic views.
base_generic_dict = {
    'paginate_by': 10,
    }

software_info_dict_date = dict(base_generic_dict,
        queryset=Software.objects.all().order_by('-pub_date'),
        template_name='software/software_list.html')

software_info_dict_software = dict(base_generic_dict,
        queryset=Software.objects.all().order_by('title'),
        template_name='software/software_list.html')

# General softwares views.
urlpatterns = patterns('',
    (r'^view/(?P<software_id>\d+)/$', software_detail),
    (r'^$', object_list, software_info_dict_date),
    (r'^date/$', object_list, software_info_dict_date),
    (r'^title/$', object_list, software_info_dict_software),
    (r'^rating/$', 'software.views.list.software_by_rating'),
    (r'^submit/', 'software.forms.add_software'),
    (r'^update/(?P<software_id>\d+)/$', 'software.forms.edit_software'),
    (r'^bib/(?P<software_id>\d+)/$', 'software.views.entry.get_bibitem'),
    (r'^paperbib/(?P<software_id>\d+)/$', 'software.views.entry.get_paperbibitem'),
    (r'^rss/latest/$', RssSoftwareFeed),
    (r'^author/$', 'software.views.entry.software_all_authors'),
    (r'^author/(?P<slug>[^/]+)/$', 'software.views.list.software_by_author'),
    (r'^users/$', 'software.views.user.user_with_software'),
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
)
