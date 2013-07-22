from django.views.generic.list import ListView
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

class SoftwareByUserView(RevisionView):
    """
    List of Software submitted by a particular User.
    """    
    def get_queryset(self):
        self.user = get_object_or_404(User, username__exact=self.kwargs["username"])
        return Revision.objects.get_by_submitter(self.user.username).order_by('-updated_date')
        
    def get_context_data(self, **kwargs):
        context = super(SoftwareByUserView, self).get_context_data(**kwargs)
        context['username'] = self.user.username
        return context
    
class SoftwareByAuthorView(RevisionView):
    """
    List of Software submitted by a particular Author
    """    
    def get_queryset(self):
        self.author = get_object_or_404(Author, slug__exact=self.kwargs["slug"])
        return Revision.objects.get_by_author(self.author.slug).order_by('-updated_date'),
        
    def get_context_data(self, **kwargs):
        context = super(SoftwareByAuthorView, self).get_context_data(**kwargs)
        context['author'] = self.author
        return context

class SoftwareByTagView(RevisionView):
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug__exact=self.kwargs["slug"])
        return Revision.objects.get_by_tag(self.tag.slug).order_by('-updated_date')

    def get_context_data(self, **kwargs):
        context = super(SoftwareByTagView, self).get_context_data(**kwargs)
        context['tags'] = self.tag
        return context

class SoftwareByLicenseView(RevisionView):
    def get_queryset(self):
        self.lic = get_object_or_404(License, slug__exact=self.kwargs["slug"])
        return Revision.objects.get_by_license(self.lic.slug).order_by('-updated_date')

    def get_context_data(self, **kwargs):
        context = super(SoftwareByLicenseView, self).get_context_data(**kwargs)
        context['os_license'] = self.lic
        return context

class SoftwareByLanguageView(RevisionView):
    """
    List of software with a particular Language
    """
    def get_queryset(self):
        self.language = get_object_or_404(Language, slug__exact=self.kwargs["slug"])
        return Revision.objects.get_by_language(self.language.slug).order_by('-updated_date')

    def get_context_data(self, **kwargs):
        context = super(SoftwareByLanguageView, self).get_context_data(**kwargs)
        context['language'] = self.language
        return context

class SoftwareByOpSysView(RevisionView):
    """
    List of software with a particular Operating System
    """
    def get_queryset(self):
        self.opsys = get_object_or_404(OpSys, slug__exact=self.kwargs["slug"])
        return Revision.objects.get_by_opsys(self.opsys.slug).order_by('-updated_date')

    def get_context_data(self, **kwargs):
        context = super(SoftwareByOpSysView, self).get_context_data(**kwargs)
        context['opsys'] = self.opsys
        return context

class SoftwareByDataFormatView(RevisionView):
    """
    List of software with a particular Operating System
    """
    def get_queryset(self):
        self.dataformat = get_object_or_404(DataFormat, slug__exact=self.kwargs["slug"])
        return Revision.objects.get_by_dataformat(self.dataformat.slug).order_by('-updated_date')

    def get_context_data(self, **kwargs):
        context = super(SoftwareByDataFormatView, self).get_context_data(**kwargs)
        context['dataformat'] = self.dataformat
        return context

class SoftwareByPubdateView(RevisionView):
    """
    List of Software ranked by first publication date
    """    
    def get_queryset(self):
        return Revision.objects.filter(revision=0).order_by('-pub_date')

class SoftwareByUpdatedDateView(RevisionView):
    """
    List of Software ranked by latest updated date
    """    
    def get_queryset(self):
        return Revision.objects.filter(revision=0).order_by('-updated_date')

class SoftwareByTitleView(RevisionView):
    """
    List of Software sorted by alphabetical order of title.
    """    
    def get_queryset(self):
        return Revision.objects.filter(revision=0).order_by('software__title', '-updated_date')

class SoftwareByViewsView(RevisionView):
    """
    List of Software ranked by views
    """    
    def get_queryset(self):
        return Revision.objects.filter(revision=0).order_by('-software__total_number_of_views','-updated_date')

class SoftwareByDownloadsView(RevisionView):
    """
    List of Software ranked by downloads
    """    
    def get_queryset(self):
        return Revision.objects.filter(revision=0).order_by('-software__total_number_of_downloads','-updated_date')

class SoftwareByRatingView(RevisionView):
    """
    List of Software ranked by rating
    """    
    def get_queryset(self):
        return Revision.objects.filter(revision=0).order_by('-software__average_rating','-updated_date')

class SoftwareBySubscriptionView(RevisionView):
    """
    List of Software ranked by rating
    """    
    def get_queryset(self):
        return Revision.objects.get_by_subscription()

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
