from django.views.generic import list_detail
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.models import User
from software.models import Software

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

def software_by_rating(request):
    """
    List of Software ranked by rating
    """
    software = Software.objects.all().order_by('-pub_date')
    sw_list=list()

    for s in software:
        r=s.get_overall_rating()
        sw_list.append((s.id,r))

    sw_list.sort(lambda x,y : cmp(x[1], y[1]))
    ids = tuple([ i[0] for i in sw_list])

    softwarelist=software.extra(where=['id IN ' + `ids`])

    return list_detail.object_list(request,
                                   paginate_by=10,
                                   queryset=softwarelist,
                                   template_name='software/software_list.html',
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

