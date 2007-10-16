"""
Views which work with Software, allowing them to be added, modified,
rated and viewed according to various criteria.

"""

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import list_detail
from django.contrib.auth.models import User

from software.models import Software

def software_detail(request, software_id):
    """
    Detail view of a Software.
    
    Context::
        object
            The Software object.
    
    Template::
        software_detail.html
    
    """
    entry = get_object_or_404(Software, pk=software_id)
    return render_to_response('software/software_detail.html',
                              { 'object': entry, },
                                context_instance=RequestContext(request))

def software_by_user(request, username):
    """
    List of Software submitted by a particular User.

    Context::
    Same as generic ``list_detail.object_list'' view, with
    one extra variable:
    
        object
            The User
    
    Template::
        software/user_detail.html
    
    """
    user = get_object_or_404(User, username__exact=username)
    return list_detail.object_list(request,
                                   queryset=Software.objects.get_by_submitter(user.username),
                                   extra_context={ 'object': user },
                                   template_name='software/user_detail.html'
                                   )
