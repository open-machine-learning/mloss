"""
Views which work with Snippets, allowing them to be added, modified,
rated and viewed according to various criteria.

"""

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import list_detail
#from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from software import forms
from software.models import Software

def snippet_detail(request, snippet_id):
    """
    Detail view of a Snippet.
    
    Context::
        object
            The Snippet object.
    
        num_ratings
            The number of Ratings this Snippet has received.
    
        rating_score
            The sum of this Snippet's received ratings.
    
    Template::
        software_detail.html
    
    """
    entry = get_object_or_404(Software, pk=snippet_id)
    return render_to_response('software_detail.html',
                              { 'object': entry, },
                                context_instance=RequestContext(request))
