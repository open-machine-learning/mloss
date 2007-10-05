"""
Views which work with Software, allowing them to be added, modified,
rated and viewed according to various criteria.

"""

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from software import forms
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
    return render_to_response('software_detail.html',
                              { 'object': entry, },
                                context_instance=RequestContext(request))
