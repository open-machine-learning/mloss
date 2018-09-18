from django.views.generic.list import ListView
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.models import User
from revision.models import Revision
from revision.models import Author, Tag, License, Language, OpSys, DataFormat
from community.summary import get_latest_news
from community.models import Forum



class ClassListView(ListView):
    """
    Create Class-based View
    """
    context_object_name='object_list'

    def get_template_names(self):
        return 'software/software_list.html'

    def get_paginate_by(self, dummy):
        return 20

class ForumClassView(ClassListView):
    def get_queryset(self, **kwargs):
        return Forum.objects.all()



class SoftwareInJmlr(ClassListView):
    """
    List Software that appeared in JMLR
    """
    def get_queryset(self, **kwargs):
        return Revision.objects.get_jmlr().order_by('-updated_date')

    def get_context_data(self, **kwargs):
        context=super(SoftwareInJmlr, self).get_context_data(**kwargs)
        context.update(get_latest_news({ 'jmlr' : True }))
        return context


class SoftwareByUser(ClassListView):
    """
    List of Software submitted by a particular User.
    """
    def get_queryset(self, **kwargs):
        username = self.kwargs['username']
        user = get_object_or_404(User, username__exact=username)
        return Revision.objects.get_by_submitter(user.username).order_by('-updated_date')
         
    def get_context_data(self, **kwargs):
        context=super(SoftwareByUser, self).get_context_data(**kwargs)
        username = self.kwargs['username']
        user = get_object_or_404(User, username__exact=username)
        context.update(get_latest_news({ 'username' : user.username }))
        return context



class SoftwareByAuthor(ClassListView):
    """
    List of software with a particular Author
    """
    def get_queryset(self, **kwargs):
        slug = self.kwargs['slug']
        author = get_object_or_404(Author, slug__exact=slug)
        return Revision.objects.get_by_author(author.slug).order_by('-updated_date')
    
    def get_context_data(self, **kwargs):
        context=super(SoftwareByAuthor, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        author = get_object_or_404(Author, slug__exact=slug)
        context.update(get_latest_news({ 'author' : author }))
        return context


class SoftwareByTag(ClassListView):
    """
    List of software with a particular Tag
    """
    def get_queryset(self, **kwargs):
        slug = self.kwargs['slug']
        tag = get_object_or_404(Tag, slug__exact=slug)
        return Revision.objects.get_by_tag(tag.slug).order_by('-updated_date')
    
    def get_context_data(self, **kwargs):
        context=super(SoftwareByTag, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        tag = get_object_or_404(Tag, slug__exact=slug)
        context.update(get_latest_news({ 'tags': tag }))
        return context



class SoftwareByLicense(ClassListView):
    """
    List of software with a particular License
    """
    def get_queryset(self, **kwargs):
        slug = self.kwargs['slug']
        lic = get_object_or_404(License, slug__exact=slug)
        return Revision.objects.get_by_license(lic.slug).order_by('-updated_date')
    
    def get_context_data(self, **kwargs):
        context=super(SoftwareByLicense, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        lic = get_object_or_404(License, slug__exact=slug)
        context.update(get_latest_news({ 'os_license' : lic }))
        return context


class SoftwareByLanguage(ClassListView):
    """
    List of software with a particular Language
    """
    def get_queryset(self, **kwargs):
        slug = self.kwargs['slug']
        language = get_object_or_404(Language, slug__exact=slug)
        return Revision.objects.get_by_language(language.slug).order_by('-updated_date')
    
    def get_context_data(self, **kwargs):
        context=super(SoftwareByLanguage, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        language = get_object_or_404(Language, slug__exact=slug)
        context.update(get_latest_news({ 'language' : language }))
        return context


class SoftwareByOpSys(ClassListView):
    """
    List of software with a particular Operating System
    """
    def get_queryset(self, **kwargs):
        slug = self.kwargs['slug']
        opsys = get_object_or_404(OpSys, slug__exact=slug)
        return Revision.objects.get_by_opsys(opsys.slug).order_by('-updated_date')
    
    def get_context_data(self, **kwargs):
        context=super(SoftwareByOpSys, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        opsys = get_object_or_404(OpSys, slug__exact=slug)
        context.update(get_latest_news({ 'opsys' : opsys }))
        return context


class SoftwareByDataFormats(ClassListView):
    """
    List of software with a particular Operating System
    """
    def get_queryset(self, **kwargs):
        slug = self.kwargs['slug']
        dataformat = get_object_or_404(DataFormat, slug__exact=slug)
        return Revision.objects.get_by_dataformat(dataformat.slug).order_by('-updated_date')
    
    def get_context_data(self, **kwargs):
        context=super(SoftwareByDataFormats, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        dataformat = get_object_or_404(DataFormat, slug__exact=slug)
        context.update(get_latest_news({ 'dataformat' : dataformat }))
        return context


class SoftwareByPubDate(ClassListView):
    """
    List of Software ranked by date
    """
    def get_queryset(self, **kwargs):
        return Revision.objects.filter(revision=0).order_by('-pub_date')
    
    def get_context_data(self, **kwargs):
        context=super(SoftwareByPubDate, self).get_context_data(**kwargs)
        context.update(get_latest_news())
        return context
    

class SoftwareByUpdatedDate(ClassListView):
    """
    List of Software ranked by date
    """
    def get_context_data(self, **kwargs):
        context=super(SoftwareByUpdatedDate, self).get_context_data(**kwargs)
        context.update(get_latest_news())
        return context

    def get_queryset(self):
	return Revision.objects.filter(revision=0).order_by('-updated_date')


class SoftwareByTitle(ClassListView):
    """
    List of Software ranked by date
    """
    def get_queryset(self, **kwargs):
        return Revision.objects.filter(revision=0).order_by('software__title','-updated_date')
        
    def get_context_data(self, **kwargs):
        context=super(SoftwareByTitle, self).get_context_data(**kwargs)
        context.update(get_latest_news())
        return context

class SoftwareByViews(ClassListView):
    """
    List of Software ranked by vies
    """
    def get_queryset(self, **kwargs):
        return Revision.objects.filter(revision=0).order_by('-software__total_number_of_views','-updated_date')
        
    def get_context_data(self, **kwargs):
        context=super(SoftwareByViews, self).get_context_data(**kwargs)
        context.update(get_latest_news())
        return context

class SoftwareByDownloads(ClassListView):
    """
    List of Software ranked by vies
    """
    def get_queryset(self, **kwargs):
        return Revision.objects.filter(revision=0).order_by('-software__total_number_of_downloads','-updated_date')
        
    def get_context_data(self, **kwargs):
        context=super(SoftwareByDownloads, self).get_context_data(**kwargs)
        context.update(get_latest_news())
        return context
                                   
class SoftwareByRating(ClassListView):
    """
    List of Software ranked by rating
    """
    def get_queryset(self, **kwargs):
        return Revision.objects.filter(revision=0).order_by('-software__average_rating','-updated_date')
        
    def get_context_data(self, **kwargs):
        context=super(SoftwareByRating, self).get_context_data(**kwargs)
        context.update(get_latest_news())
        return context

class SoftwareBySubscription(ClassListView):
    """
    List of Software ranked by number of subscription
    """
    def get_queryset(self, **kwargs):
        return Revision.objects.get_by_subscription()
        
    def get_context_data(self, **kwargs):
        context=super(SoftwareBySubscription, self).get_context_data(**kwargs)
        context.update(get_latest_news())
        return context

##TODO
def search_description(request, qs):
    if qs.count()==0:
        return render_to_response('software/software_list.html',
                get_latest_news({ 'search_term': qs }),RequestContext(request))
    else:
        pass #return ClassListView(Revision.objects.get_by_searchterm(q), get_latest_news({ 'search_term': q }))
