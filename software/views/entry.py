"""
Views which work with Software, allowing them to be added, modified,
rated and viewed according to various criteria.

"""

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from software.models import Software, SoftwareRating, SoftwareStatistics
from software.forms import RatingForm
from django.http import HttpResponse
from django.contrib.sites.models import Site
from django.views.generic import list_detail
from software.models import Author, Tag, License, Language, OpSys


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
    entry.update_views()
    todays_stats = entry.get_stats_for_today()

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
            { 'object': entry,
                'ratingform': ratingform,
                'todays_stats' : todays_stats},
			context_instance=RequestContext(request))

def get_bibitem(request, software_id):
    entry = get_object_or_404(Software, pk=software_id)
    key=''
    authors=''
    author_list = entry.authors.split(',')
    for i in xrange(len(author_list)):
        a=author_list[i]
        key+=a.split(' ')[-1][:3]
        authors+=a.strip()
        if i<len(author_list)-1:
            authors += ' and '

    key+= `entry.pub_date.year`[2:4]

    response = HttpResponse(mimetype='application/text')
    response['Content-Disposition'] = 'attachment; filename=%s.bib' % key
    response.write(u"@misc{%s,\n author={%s},\n title={%s},\n year={%s},\n note={\\url{%s}}\n}" %
            (key,
            authors,
            entry.title,
            `entry.pub_date.year`,
            'http://' + Site.objects.get_current().domain + entry.get_absolute_url()))
    return response

def get_paperbibitem(request, software_id):
    entry = get_object_or_404(Software, pk=software_id)
    key=''
    author_list = entry.authors.split(',')
    for i in xrange(len(author_list)):
        a=author_list[i]
        key+=a.split(' ')[-1][:3]

    key+= `entry.pub_date.year`[2:4]

    response = HttpResponse(mimetype='application/text')
    response['Content-Disposition'] = 'attachment; filename=%s_paper.bib' % key
    response.write("%s" % entry.paper_bib)
    return response

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



def software_all_authors(request):
    authorlist = Author.objects.filter(name__isnull=False).distinct()
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=authorlist,
                                   template_name='software/author_list.html',
                                   )


def software_all_tags(request):
    taglist = Tag.objects.filter(name__isnull=False).distinct()
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=taglist,
                                   template_name='software/tag_list.html',
                                   )


def software_all_licenses(request):
    licenselist = License.objects.filter(name__isnull=False).distinct()
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=licenselist,
                                   template_name='software/license_list.html',
                                   )


def software_all_languages(request):
    languagelist = Language.objects.filter(name__isnull=False).distinct()
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=languagelist,
                                   template_name='software/language_list.html',
                                   )


def software_all_opsyss(request):
    opsyslist = OpSys.objects.filter(name__isnull=False).distinct()
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=opsyslist,
                                   template_name='software/opsys_list.html',
                                   )


