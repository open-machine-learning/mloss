list_detail.object_listfrom django.views.generic.list import ListView
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.models import User
from revision.models import Revision
from revision.models import Author, Tag, License, Language, OpSys, DataFormat
from community.summary import get_latest_news

# TODO: need to move to class based views

class RevisionView(ListView):
    """
    View details of software
    """
    #context_object_name = 'revision'
    template_name = 'software/software_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(RevisionView, self).get_context_data(**kwargs)
        all_context = get_latest_news(context)
        return all_context

class SoftwareInJMLRView(RevisionView):
    """
    List Software that appeared in JMLR
    """    
    def get_queryset(self):
        return Revision.objects.get_jmlr().order_by('-updated_date')
        
    def get_context_data(self, **kwargs):
        context = super(SoftwareInJMLRView, self).get_context_data(**kwargs)
        context['jmlr'] = True
        return context

def software_in_jmlr(request):
    """
    Deprecated. List Software that appeared in JMLR
    """
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=Revision.objects.get_jmlr().order_by('-updated_date'),
                                   extra_context=get_latest_news({ 'jmlr' : True }),
                                   template_name='software/software_list.html'
                                   )

class SoftwareByUserView(RevisionView):
    """
    List of Software submitted by a particular User.
    """    
    def get_queryset(self):
        self.user = get_object_or_404(User, username__exact=self.args[0])
        return Revision.objects.get_by_submitter(self.user.username).order_by('-updated_date')
        
    def get_context_data(self, **kwargs):
        context = super(SoftwareByUserView, self).get_context_data(**kwargs)
        context['username'] = self.user.username
        return context

    
def software_by_user(request, username):
    """
    Deprecated. List of Software submitted by a particular User.
    """
    user = get_object_or_404(User, username__exact=username)
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=Revision.objects.get_by_submitter(user.username).order_by('-updated_date'),
                                   extra_context=get_latest_news({ 'username' : user.username }),
                                   template_name='software/software_list.html'
                                   )

class SoftwareByAuthorView(RevisionView):
    """
    List of Software submitted by a particular Author
    """    
    def get_queryset(self):
        self.author = get_object_or_404(Author, slug__exact=self.args[0])
        return Revision.objects.get_by_author(author.slug).order_by('-updated_date'),
        
    def get_context_data(self, **kwargs):
        context = super(SoftwareByUserView, self).get_context_data(**kwargs)
        context['author'] = self.author
        return context

def software_by_author(request, slug):
    """
    Deprecated. List of software with a particular Author
    """
    author = get_object_or_404(Author, slug__exact=slug)
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=Revision.objects.get_by_author(author.slug).order_by('-updated_date'),
                                   extra_context=get_latest_news({ 'author' : author }),
                                   template_name='software/software_list.html',
                                   )

def software_by_tag(request, slug):
    """
    List of software with a particular Tag
    """
    tag = get_object_or_404(Tag, slug__exact=slug)
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=Revision.objects.get_by_tag(tag.slug).order_by('-updated_date'),
                                   extra_context=get_latest_news({ 'tags': tag }),
                                   template_name='software/software_list.html',
                                   )

def software_by_license(request, slug):
    """
    List of software with a particular License
    """
    lic = get_object_or_404(License, slug__exact=slug)
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=Revision.objects.get_by_license(lic.slug).order_by('-updated_date'),
                                   extra_context=get_latest_news({ 'os_license' : lic }),
                                   template_name='software/software_list.html',
                                   )

def software_by_language(request, slug):
    """
    List of software with a particular Language
    """
    language = get_object_or_404(Language, slug__exact=slug)
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=Revision.objects.get_by_language(language.slug).order_by('-updated_date'),
                                   extra_context=get_latest_news({ 'language' : language }),
                                   template_name='software/software_list.html',
                                   )

def software_by_opsys(request, slug):
    """
    List of software with a particular Operating System
    """
    opsys = get_object_or_404(OpSys, slug__exact=slug)
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=Revision.objects.get_by_opsys(opsys.slug).order_by('-updated_date'),
                                   extra_context=get_latest_news({ 'opsys' : opsys }),
                                   template_name='software/software_list.html',
                                   )

def software_by_dataformats(request, slug):
    """
    List of software with a particular Operating System
    """
    dataformat = get_object_or_404(DataFormat, slug__exact=slug)
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=Revision.objects.get_by_dataformat(dataformat.slug).order_by('-updated_date'),
                                   extra_context=get_latest_news({ 'dataformat' : dataformat }),
                                   template_name='software/software_list.html',
                                   )

class SoftwareByPubdateView(RevisionView):
    """
    List of Software ranked by first publication date
    """    
    def get_queryset(self):
        return Revision.objects.filter(revision=0).order_by('-pub_date')

def software_by_pub_date(request):
    """
    Deprecated. List of Software ranked by date
    """

    softwarelist = Revision.objects.filter(revision=0).order_by('-pub_date')

    return list_detail.object_list(request,
                                   paginate_by=10,
                                   queryset=softwarelist,
                                   template_name='software/software_list.html',
                                   extra_context=get_latest_news(),
                                   )

class SoftwareByUpdatedDateView(RevisionView):
    """
    List of Software ranked by latest updated date
    """    
    def get_queryset(self):
        return Revision.objects.filter(revision=0).order_by('-updated_date')

def software_by_updated_date(request):
    """
    Deprecated. List of Software ranked by date
    """

    softwarelist = Revision.objects.filter(revision=0).order_by('-updated_date')

    return list_detail.object_list(request,
                                   paginate_by=10,
                                   queryset=softwarelist,
                                   template_name='software/software_list.html',
                                   extra_context=get_latest_news(),
                                   )

class SoftwareByTitleView(RevisionView):
    """
    List of Software sorted by alphabetical order of title.
    """    
    def get_queryset(self):
        return Revision.objects.filter(revision=0).order_by('software__title', '-updated_date')

def software_by_title(request):
    """
    Deprecated. List of Software ranked by date
    """

    softwarelist = Revision.objects.filter(revision=0).order_by('software__title','-updated_date')

    return list_detail.object_list(request,
                                   paginate_by=10,
                                   queryset=softwarelist,
                                   template_name='software/software_list.html',
                                   extra_context=get_latest_news(),
                                   )

class SoftwareByViewsView(RevisionView):
    """
    List of Software ranked by views
    """    
    def get_queryset(self):
        return Revision.objects.filter(revision=0).order_by('-software__total_number_of_views','-updated_date')

    
def software_by_views(request):
    """
    Deprecated. List of Software ranked by vies
    """

    softwarelist = Revision.objects.filter(revision=0).order_by('-software__total_number_of_views','-updated_date')

    return list_detail.object_list(request,
                                   paginate_by=10,
                                   queryset=softwarelist,
                                   template_name='software/software_list.html',
                                   extra_context=get_latest_news(),
                                   )

class SoftwareByDownloadsView(RevisionView):
    """
    List of Software ranked by downloads
    """    
    def get_queryset(self):
        return Revision.objects.filter(revision=0).order_by('-software__total_number_of_downloads','-updated_date')

def software_by_downloads(request):
    """
    Deprecated. List of Software ranked by downloads
    """

    softwarelist = Revision.objects.filter(revision=0).order_by('-software__total_number_of_downloads','-updated_date')

    return list_detail.object_list(request,
                                   paginate_by=10,
                                   queryset=softwarelist,
                                   template_name='software/software_list.html',
                                   extra_context=get_latest_news(),
                                   )

class SoftwareByRatingView(RevisionView):
    """
    List of Software ranked by rating
    """    
    def get_queryset(self):
        return Revision.objects.filter(revision=0).order_by('-software__average_rating','-updated_date')

def software_by_rating(request):
    """
    Deprecated. List of Software ranked by rating
    """
    softwarelist = Revision.objects.filter(revision=0).order_by('-software__average_rating','-updated_date')

    return list_detail.object_list(request,
                                   paginate_by=10,
                                   queryset=softwarelist,
                                   template_name='software/software_list.html',
                                   extra_context=get_latest_news(),
                                   )

def software_by_subscription(request):
    """
    List of Software ranked by number of subscription
    """
    softwarelist = Revision.objects.get_by_subscription()

    return list_detail.object_list(request,
                                   paginate_by=10,
                                   queryset=softwarelist,
                                   template_name='software/software_list.html',
                                   extra_context=get_latest_news(),
                                   )

def search_description(request, q):
    qs=Revision.objects.get_by_searchterm(q)
    if qs.count()==0:
        return render_to_response('software/software_list.html',
                get_latest_news({ 'search_term': q }),
                context_instance=RequestContext(request))
    else:
        return list_detail.object_list(request,
                                   paginate_by=10,
                                   queryset=qs,
                                   template_name='software/software_list.html',
                                   extra_context=get_latest_news({ 'search_term': q }),
                                   )
