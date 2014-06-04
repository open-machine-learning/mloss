from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.sites.models import Site

from revision.models import Revision
from software.models import Software, SoftwareRating
from software.forms import RatingForm

def revision_detail(request, revision_id):
    revision = get_object_or_404(Revision, pk=revision_id)
    software = revision.software
    revisions = Revision.objects.filter(software=software)
    todays_stats = software.update_views()

    if revisions.count() <= 1:
        revisions = None

    ratingform = None

    if request.user.is_authenticated() and not request.user == software.user:
        try:
            r = SoftwareRating.objects.get(user__id=request.user.id, software=software)
            ratingform= RatingForm({'features': r.features,
                'usability': r.usability,
                'documentation': r.documentation})

        except SoftwareRating.DoesNotExist:
            ratingform = RatingForm()
    
    return render_to_response('software/software_detail.html',
            { 'object': revision,
                'ratingform': ratingform,
                'todays_stats' : todays_stats,
				'revision' : '/' + str(revision.id),
                'revisions' : revisions },
            context_instance=RequestContext(request))

def download_revision(request, revision_id):
    entry = get_object_or_404(Revision, pk=revision_id)
    sw = get_object_or_404(Software, pk=entry.software.pk)
    sw.update_downloads()

    if entry.download_url:
        return HttpResponseRedirect(entry.download_url)
    elif entry.tarball:
        return HttpResponseRedirect('/media/' + entry.tarball.name)
    else:
        raise Http404

def view_homepage(request, revision_id):
    entry = get_object_or_404(Revision, pk=revision_id)
    sw = get_object_or_404(Software, pk=entry.software.pk)
    sw.update_views()
    return HttpResponseRedirect(entry.project_url)

def view_jmlr_homepage(request, revision_id):
    entry = get_object_or_404(Revision, pk=revision_id)
    sw = get_object_or_404(Software, pk=entry.software.pk)
    sw.update_views()
    return HttpResponseRedirect(entry.jmlr_mloss_url)

def get_bibitem(request, revision_id):
    entry = get_object_or_404(Revision, pk=revision_id)
    sw = get_object_or_404(Software, pk=entry.software.pk)
    sw.update_views()
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
            sw.title,
            `entry.pub_date.year`,
            'http://' + Site.objects.get_current().domain + sw.get_absolute_url()))
    return response

def get_paperbibitem(request, revision_id):
    entry = get_object_or_404(Revision, pk=revision_id)
    sw = get_object_or_404(Software, pk=entry.software.pk)
    sw.update_views()
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

