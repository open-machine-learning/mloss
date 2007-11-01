"""
Views which work with Software, allowing them to be added, modified,
rated and viewed according to various criteria.

"""

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import list_detail
from django.contrib.auth.models import User

from software.models import Software, SoftwareRating

from software.forms import RatingForm

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
    ratingform = None

    if request.user.is_authenticated() and not request.user == entry.user:
        try:
            r = SoftwareRating.objects.get(user__id=request.user.id, software=entry)
            ratingform= RatingForm({'features': r.features,
                'usability': r.usability,
                'documentation': r.documentation})

        except SoftwareRating.DoesNotExist:
            ratingform = RatingForm()
    
    return render_to_response('software/software_detail.html',
                { 'object': entry, 'ratingform': ratingform },
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
                                   paginate_by=10,
                                   queryset=Software.objects.get_by_submitter(user.username),
                                   extra_context={ 'object': user },
                                   template_name='software/software_list.html'
                                   )
def software_by_license(request, license):
    """
    List of Software submitted with a particular License.

    Context::
    Same as generic ``list_detail.object_list'' view, with
    one extra variable:
    
        object
            The User
    
    Template::
        software/user_detail.html
    
    """
    return list_detail.object_list(request,
                                   paginate_by=10,
                                   queryset=Software.objects.get_by_license(license),
                                   template_name='software/software_list.html',
                                   extra_context={ 'os_license': license },
                                   )

def software_by_language(request, language):
    """
    List of Software submitted with a particular License.

    Context::
    Same as generic ``list_detail.object_list'' view, with
    one extra variable:
    
        object
            The User
    
    Template::
        software/user_detail.html
    
    """
    return list_detail.object_list(request,
                                   paginate_by=10,
                                   queryset=Software.objects.get_by_language(language),
                                   template_name='software/software_list.html',
                                   extra_context={ 'language': language },
                                   )

def search_description(request, q):
    """
    List of Software submitted with a particular License.

    Context::
    Same as generic ``list_detail.object_list'' view, with
    one extra variable:
    
        object
            The User
    
    Template::
        software/user_detail.html
    
    """
    qs=Software.objects.get_by_searchterm(q)
    if qs.count()==0:
        return render_to_response('software/software_list.html',
                              { 'search_term': q, },
                                context_instance=RequestContext(request))
    else:
        return list_detail.object_list(request,
                                   paginate_by=10,
                                   queryset=qs,
                                   template_name='software/software_list.html',
                                   extra_context={ 'search_term': q },
                                   )

def rate(request, software_id):
    software = get_object_or_404(Software, pk=software_id)
    if request.user.is_authenticated() and not request.user == software.user:
        if request.method == 'POST':
            form=RatingForm(request.POST)
            if form.is_valid():
                try:
                    r = SoftwareRating.objects.get(user=request.user, software=software)
                    r.features = form.cleaned_data['features']
                    r.usability = form.cleaned_data['usability']
                    r.documentation = form.cleaned_data['documentation']
                    r.save()
                except SoftwareRating.DoesNotExist:
                    r, fail = SoftwareRating.objects.get_or_create(user=request.user,
                            software=software,
                            features = form.cleaned_data['features'],
                            usability = form.cleaned_data['usability'],
                            documentation = form.cleaned_data['documentation'])
                    r.save()
    return software_detail(request, software_id)
