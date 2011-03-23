"""
Views which work with Software, allowing them to be added, modified,
rated and viewed according to various criteria.

"""

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.contrib.comments.forms import CommentForm
from django.views.generic import list_detail

from revision.models import Revision, Author, Tag, License, Language, OpSys, DataFormat
from software.models import Software, SoftwareRating, SoftwareStatistics
from software.forms import RatingForm
from subscriptions.models import Subscriptions
from community.views import get_latest_news

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
    software = get_object_or_404(Software, pk=software_id)
    revisions = Revision.objects.filter(software=software)
    entry = get_object_or_404(revisions, revision=0)
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
            { 'object': entry,
                'ratingform': ratingform,
                'todays_stats' : todays_stats,
                'revisions' : revisions },
            context_instance=RequestContext(request))


def subscribe_software(request, software_id, bookmark=False):
    if not request.user.is_authenticated():
       return HttpResponseRedirect('/accounts/login?next=%s' % request.path)
    entry = get_object_or_404(Software, pk=software_id)
    entry.subscribe(request.user, bookmark)

    return HttpResponseRedirect("/user/view/" + str(request.user.id) + "/")

def bookmark_software(request, software_id):
    return subscribe_software(request, software_id, bookmark=True)

def unsubscribe_software(request, software_id, bookmark=False):
    if not request.user.is_authenticated():
       return HttpResponseRedirect('/accounts/login?next=%s' % request.path)
    entry = get_object_or_404(Software, pk=software_id)
    entry.unsubscribe(request.user, bookmark)

    return HttpResponseRedirect("/user/view/" + str(request.user.id) + "/")

def remove_bookmark(request, software_id):
    return unsubscribe_software(request, software_id, bookmark=True)

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
                                   extra_context=get_latest_news(),
                                   )


def software_all_tags(request):
    taglist = Tag.objects.filter(name__isnull=False).distinct().order_by('slug')
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=taglist,
                                   template_name='software/tag_list.html',
                                   extra_context=get_latest_news(),
                                   )


def software_all_licenses(request):
    licenselist = License.objects.filter(name__isnull=False).distinct().order_by('slug')
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=licenselist,
                                   template_name='software/license_list.html',
                                   extra_context=get_latest_news(),
                                   )


def software_all_languages(request):
    languagelist = Language.objects.filter(name__isnull=False).distinct().order_by('slug')
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=languagelist,
                                   template_name='software/language_list.html',
                                   extra_context=get_latest_news(),
                                   )


def software_all_opsyss(request):
    opsyslist = OpSys.objects.filter(name__isnull=False).distinct().order_by('slug')
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=opsyslist,
                                   template_name='software/opsys_list.html',
                                   extra_context=get_latest_news(),
                                   )

def software_all_dataformats(request):
    dataformatlist = DataFormat.objects.filter(name__isnull=False).distinct().order_by('slug')
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=dataformatlist,
                                   template_name='software/dataformat_list.html',
                                   extra_context=get_latest_news(),
                                   )

def user_with_software(request):
    userlist = User.objects.filter(software__isnull=False).distinct().order_by('username')
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=userlist,
                                   template_name='software/user_list.html',
                                   extra_context=get_latest_news(),
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
    from matplotlib.dates import DayLocator, WeekdayLocator, HourLocator, MonthLocator, YearLocator
    from matplotlib.dates import DateFormatter, date2num
    from StringIO import StringIO

    if dpi<=40:
        bgcol='#f7f7f7'
    else:
        bgcol='#ffffff'
    fig = Figure(figsize=(8,6), dpi=dpi, facecolor=bgcol)
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)

    stat = SoftwareStatistics.objects.filter(software=software_id).distinct().order_by('date')

    if stat.count()<=0:
        return HttpResponseForbidden()

    x=list()
    y=list()
    for entry in stat:
        x.append(date2num(entry.date))
        if type=='downloads':
            y.append(entry.number_of_downloads)
        elif type=='views':
            y.append(entry.number_of_views)

    #ax.plot(x,y,'bo', alpha=0.7)
    #ax.plot(x,y,'b-',linewidth=1, alpha=0.5)
    ax.bar(x,y)

    days = DayLocator()
    weeks= WeekdayLocator()
    months= MonthLocator()
    years= YearLocator()
    dateFmt = DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(dateFmt)

    if len(x)<=14:
        ax.xaxis.set_major_locator(days)
    elif len(x)<60:
        ax.xaxis.set_major_locator(weeks)
        ax.xaxis.set_minor_locator(days)
    elif len(x)<720:
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_minor_locator(weeks)
    else:
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_minor_locator(months)

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
    del fig
    del ax

    return HttpResponse(imdata.getvalue(), mimetype='image/png')

def downloadstats(request, software_id):
    return stats_helper(request, software_id, 'downloads', 80)

def viewstats(request, software_id):
    return stats_helper(request, software_id, 'views', 80)

def downloadstatspreview(request, software_id):
    return stats_helper(request, software_id, 'downloads', 17)

def viewstatspreview(request, software_id):
    return stats_helper(request, software_id, 'views', 17)

