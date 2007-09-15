"""
URLConf for software.

Recommended usage is to use a call to ``include("software.urls")`` in your project's
root URLConf to include this URLConf for any URL beginning with
'/browse/'.

"""

from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list
from models import Author, Software
from views import entry


# Info for generic views.
base_generic_dict = {
    'paginate_by': 10,
    }


software_info_dict = dict(base_generic_dict,
                          queryset=Software.objects.all(),
                          template_name='software_list.html')

author_info_dict = dict(base_generic_dict,
                        queryset=Author.objects.all(),
                        template_name='author_list.html')

# General snippets views.
urlpatterns = patterns('',
                       (r'^(?P<snippet_id>\d+)/$', entry.snippet_detail),
                       )

# Generic views.
urlpatterns += patterns('',
                        (r'^$', object_list, software_info_dict),
                        (r'^authors/$', object_list, author_info_dict),
                        )
