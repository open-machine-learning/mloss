"""
Views which work with Software, allowing them to be added, modified,
rated and viewed according to various criteria.

"""

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.views.generic import list_detail

from software.models import Software, SoftwareRating, SoftwareStatistics
from software.models import Author, Tag, License, Language, OpSys
from software.forms import RatingForm
from subscriptions.models import Subscriptions

import settings

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
    todays_stats = entry.update_views()

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


def subscribe_software(request, software_id, bookmark=False):
    if not request.user.is_authenticated():
       return HttpResponseRedirect('/accounts/login?next=%s' % request.path)
    entry = get_object_or_404(Software, pk=software_id)

    ctype = ContentType.objects.get_for_model(entry)
    Subscriptions.objects.get_or_create(title="Software " + entry.title,
            content_type=ctype, object_id=entry.id, user=request.user,
            url=entry.get_absolute_url(), bookmark=bookmark)

    return HttpResponseRedirect("/user/view/" + str(request.user.id) + "/")

def bookmark_software(request, software_id):
    return subscribe_software(request, software_id, bookmark=True)

def unsubscribe_software(request, software_id, bookmark=False):
    if not request.user.is_authenticated():
       return HttpResponseRedirect('/accounts/login?next=%s' % request.path)
    entry = get_object_or_404(Software, pk=software_id)

    ctype = ContentType.objects.get_for_model(entry)
    object=get_object_or_404(Subscriptions, content_type=ctype, object_id=entry.id,
            user=request.user, bookmark=bookmark)
    object.delete()

    return HttpResponseRedirect("/user/view/" + str(request.user.id) + "/")

def remove_bookmark(request, software_id):
    return unsubscribe_software(request, software_id, bookmark=True)

def download_software(request, software_id):
    entry = get_object_or_404(Software, pk=software_id)
    entry.update_downloads()

    if entry.download_url:
        return HttpResponseRedirect(entry.download_url)
    elif entry.tarball:
        return HttpResponseRedirect('/media/' + entry.tarball)
    else:
        raise Http404

def view_homepage(request, software_id):
    entry = get_object_or_404(Software, pk=software_id)
    entry.update_views()
    return HttpResponseRedirect(entry.project_url)

def view_jmlr_homepage(request, software_id):
    entry = get_object_or_404(Software, pk=software_id)
    entry.update_views()
    return HttpResponseRedirect(entry.jmlr_mloss_url)

def get_bibitem(request, software_id):
    entry = get_object_or_404(Software, pk=software_id)
    entry.update_views()
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
    entry.update_views()
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
                    r.update_rating(form.cleaned_data['features'],
                            form.cleaned_data['usability'],
                            form.cleaned_data['documentation'])
                except SoftwareRating.DoesNotExist:
                    r, fail = SoftwareRating.objects.get_or_create(user=request.user, software=software)
                    r.update_rating(form.cleaned_data['features'],
                            form.cleaned_data['usability'],
                            form.cleaned_data['documentation'])

    return software_detail(request, software_id)



def software_all_authors(request):
    authorlist = Author.objects.filter(name__isnull=False).distinct().order_by('slug')
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=authorlist,
                                   template_name='software/author_list.html',
                                   )


def software_all_tags(request):
    taglist = Tag.objects.filter(name__isnull=False).distinct().order_by('slug')
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=taglist,
                                   template_name='software/tag_list.html',
                                   )


def software_all_licenses(request):
    licenselist = License.objects.filter(name__isnull=False).distinct().order_by('slug')
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=licenselist,
                                   template_name='software/license_list.html',
                                   )


def software_all_languages(request):
    languagelist = Language.objects.filter(name__isnull=False).distinct().order_by('slug')
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=languagelist,
                                   template_name='software/language_list.html',
                                   )


def software_all_opsyss(request):
    opsyslist = OpSys.objects.filter(name__isnull=False).distinct().order_by('slug')
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=opsyslist,
                                   template_name='software/opsys_list.html',
                                   )

def user_with_software(request):
    userlist = User.objects.filter(software__isnull=False).distinct().order_by('username')
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=userlist,
                                   template_name='software/user_list.html',
                                   )

def stats_helper(request, software_id, type, dpi):
    # matplotlib needs a writable home directory
    if settings.PRODUCTION:
        import os
        os.environ['HOME']='/home/mloss/tmp'

    import matplotlib
    import datetime
    matplotlib.use('Cairo')
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_cairo import FigureCanvasCairo as FigureCanvas
    from matplotlib.dates import DayLocator, WeekdayLocator, HourLocator, DateFormatter, date2num
    from StringIO import StringIO

    if dpi<=40:
        bgcol='#f7f7f7'
    else:
        bgcol='#ffffff'
    fig = Figure(figsize=(8,5), dpi=dpi, facecolor=bgcol)
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)

    stat = SoftwareStatistics.objects.filter(software=software_id).distinct().order_by('date')

    x=list()
    y=list()
    for entry in stat:
        x.append(date2num(entry.date))
        if type=='downloads':
            y.append(entry.number_of_downloads)
        elif type=='views':
            y.append(entry.number_of_views)

    ax.bar(x,y)

    days = DayLocator()
    weeks= WeekdayLocator()
    dateFmt = DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(dateFmt)

    if len(x)<=14:
        ax.xaxis.set_major_locator(days)
    elif len:
        ax.xaxis.set_major_locator(weeks)
        ax.xaxis.set_minor_locator(days)

    if dpi>40:
        if type=='downloads':
            ax.set_title('Number of Downloads')
            ax.set_ylabel('Downloads per Day')
        elif type=='views':
            ax.set_title('Number of Views')
            ax.set_ylabel('Views per Day')

        ax.grid(True)

    ax.axis("tight")
    for label in ax.get_xticklabels():
        label.set_ha('right')
        label.set_rotation(30)

    canvas.draw()
    imdata=StringIO()
    fig.savefig(imdata,format='png', dpi=dpi, facecolor=bgcol)
    return HttpResponse(imdata.getvalue(), mimetype='image/png')

def downloadstats(request, software_id):
    return stats_helper(request, software_id, 'downloads', 80)

def viewstats(request, software_id):
    return stats_helper(request, software_id, 'views', 80)

def downloadstatspreview(request, software_id):
    return stats_helper(request, software_id, 'downloads', 17)

def viewstatspreview(request, software_id):
    return stats_helper(request, software_id, 'views', 17)

