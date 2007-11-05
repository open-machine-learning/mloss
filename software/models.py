from django.db import models
import datetime
from markdown import markdown
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


# make sure this list of variables is up-to-date (i.e. matches
# the fields in the Software object
editables=('version','authors',
        'contact', 'description', 'project_url', 'tags', 'language',
        'os_license', 'tarball', 'screenshot', 'operating_systems',
        'paper_bib')

# don't change db of the following fields if they are empty
dontupdateifempty=['tarball', 'screenshot']

class SoftwareManager(models.Manager):
    """
    Custom manager for the Software model.
    
    Adds shortcuts for common filtering operations, and for retrieving
    popular related objects.
    
    """
    def get_by_submitter(self, username):
        """
        Returns a QuerySet of Software submitted by a particular User.
        
        """
        return self.filter(user__username__exact=username)

    def get_by_license(self, license):
        """
        Returns a QuerySet of Software sorted by a particular license.
        
        """
        return self.filter(os_license__exact=license)

    def get_by_language(self, language):
        """
        Returns a QuerySet of Software sorted by a particular language.
        
        """
        return self.filter(language__exact=language)

    def get_by_searchterm(self, searchterm):
        """
        Returns a QuerySet of Software matching the searchterm
        
        """
        return self.filter(
                Q(user__username__icontains=searchterm) |
                Q(title__icontains=searchterm) |
                Q(version__icontains=searchterm) |
                Q(authors__icontains=searchterm) |
                Q(description__icontains=searchterm) |
                Q(tags__icontains=searchterm) |
                Q(language__icontains=searchterm) |
                Q(operating_systems__icontains=searchterm) |
                Q(os_license__icontains=searchterm))

    
# Create your models here.
class Software(models.Model):
    """
    A description of some machine learning open source
    software project.
    """
    user = models.ForeignKey(User, raw_id_admin=True)
    title = models.CharField(max_length=80)
    version = models.CharField(max_length=80)
    authors = models.CharField(max_length=200)
    contact = models.EmailField(max_length=80)
    description = models.TextField()
    description_html = models.TextField(editable=False)
    project_url = models.URLField(verify_exists=False)
    jmlr_mloss_url = models.URLField(verify_exists=False, blank=True)
    tags = models.CharField(max_length=200,blank=True)
    language = models.CharField(max_length=200,blank=True)
    os_license = models.CharField(max_length=200)
    operating_systems = models.CharField(max_length=200)
    paper_bib = models.TextField(blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()
    tarball = models.FileField(upload_to="code_archive/",blank=True,null=True)
    average_rating = models.FloatField(editable=False, blank=True, null=True)

    try:
        from PIL import Image  
        screenshot = models.ImageField(upload_to="screenshot_archive/",blank=True,null=True)
    except ImportError:
        screenshot = models.FileField(upload_to="screenshot_archive/",blank=True,null=True)
       

    objects = SoftwareManager()

    def get(self, a, b):
        return self.__dict__[a]

    def save(self, auto_update_date=True):
        if not self.id:
            self.pub_date = datetime.datetime.now()
        if auto_update_date:
            self.updated_date = datetime.datetime.now()

        # Use safe_mode in Markdown to prevent arbitrary input
        # and strip all html tags from CharFields
        self.title = strip_tags(self.title)
        self.version = strip_tags(self.version)
        self.authors = strip_tags(self.authors)
        self.description_html = markdown(self.description, safe_mode=True)
        self.tags = strip_tags(self.tags)
        self.language = strip_tags(self.language)
        self.os_license = strip_tags(self.os_license)
        self.paper_bib = strip_tags(self.paper_bib)
        self.operating_systems = strip_tags(self.operating_systems)
        super(Software, self).save()

    def get_taglist(self):
        return [x.strip().encode('utf-8') for x in self.tags.split(',')]

    def get_description_page(self):
        s="<html>" + self.description_html + "</html>"
        return s.encode('utf-8')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return ('software.views.entry.software_detail', (), { 'software_id': str(self.id) })

    get_absolute_url = models.permalink(get_absolute_url)

    class Admin:
        fields = (
            ('Metadata', {
            'fields': ('user', 'title', 'version', 'authors')}),
            ('None', {
            'fields': ( 'contact', 'description',
				'project_url', 'jmlr_mloss_url', 'tags', 'language', 'os_license', 
				'pub_date', 'updated_date', 'tarball', 'screenshot', 'operating_systems',
				'paper_bib')}),
            )
        list_filter = ['pub_date']
        date_hierarchy = 'pub_date'
        search_fields = ['title']

    def get_overall_rating(self):
        """get_ratings(self) -> mean(features, usability, documentation)

        return the average of all ratings or None if no ratings
        have been given so far.""" 
        ratings = SoftwareRating.objects.filter(software=self)
        l = float(len(ratings))
        if l > 0.0:
            return sum([ r.features+r.usability+r.documentation for r in ratings])/(3*l)
        else:
            return -1

    def get_ratings(self):
        """get_ratings(self) -> features, usability, documentation

        return the average ratings or [None, None, None] if no ratings
        have been given so far.""" 
        ratings = SoftwareRating.objects.filter(software=self)
        l = float(len(ratings))
        if l > 0.0:
            features = sum([ r.features for r in ratings])/l
            usability = sum([ r.usability for r in ratings])/l
            documentation = sum([ r.documentation for r in ratings])/l
            return features, usability, documentation
        else:
            return None, None, None

    def get_features_rating(self):
        ratings = SoftwareRating.objects.filter(software=self)
        l = float(ratings.count())
        if l > 0.0:
            return sum([ r.features for r in ratings])/l            

    def get_documentation_rating(self):
        ratings = SoftwareRating.objects.filter(software=self)
        l = float(ratings.count())
        if l > 0.0:
            return sum([ r.documentation for r in ratings])/l            

    def get_usability_rating(self):
        ratings = SoftwareRating.objects.filter(software=self)
        l = float(ratings.count())
        if l > 0.0:
            return sum([ r.usability for r in ratings])/l            

    def get_num_votes(self):
        return float(SoftwareRating.objects.filter(software=self).count())

    class Meta:
        ordering = ('-pub_date',)

class SoftwareRating(models.Model):
    """Rating for a software

    Each user can rate a software only once (but she might change
    her rating?)"""
    user = models.ForeignKey(User, raw_id_admin=True)
    software = models.ForeignKey(Software)
    features = models.IntegerField()
    usability = models.IntegerField()
    documentation = models.IntegerField()

    class Admin:
        pass
