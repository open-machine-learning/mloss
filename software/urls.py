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

software_info_dict_author = dict(base_generic_dict,
		queryset=Software.objects.all().order_by('authors'),
		template_name='software/software_list.html')

software_info_dict_submitter = dict(base_generic_dict,
		queryset=Software.objects.all().order_by('user'),
		template_name='software/software_list.html')

software_info_dict_tags = dict(base_generic_dict,
		queryset=Software.objects.all().order_by('tags'),
		template_name='software/software_list.html')

software_info_dict_license = dict(base_generic_dict,
		queryset=Software.objects.all().order_by('os_license'),
		template_name='software/software_list.html')


# General softwares views.
urlpatterns = patterns('',
    (r'^view/(?P<software_id>\d+)/$', software_detail),
    (r'^$', object_list, software_info_dict_date),
    (r'^date/$', object_list, software_info_dict_date),
    (r'^title/$', object_list, software_info_dict_software),
    (r'^author/$', object_list, software_info_dict_author),
    (r'^submitter/$', object_list, software_info_dict_submitter),
    (r'^tags/$', object_list, software_info_dict_tags),
    (r'^submit/', 'software.forms.add_software'),
    (r'^update/(?P<software_id>\d+)/$', 'software.forms.edit_software'),
	(r'^rss/latest/$', RssSoftwareFeed),
    (r'^users/$', 'software.views.user.user_with_software'),
    (r'^users/(?P<username>[^/]+)/$', 'software.views.entry.software_by_user'),
    (r'^license/$', 'software.views.license.license_with_software'),
    (r'^license/(?P<license>[^/]+)/$', 'software.views.entry.software_by_license'),
    (r'^language/$', 'software.views.language.language_with_software'),
    (r'^language/(?P<language>[^/]+)/$', 'software.views.entry.software_by_language'),
)
