from django.db import models
import datetime
from markdown import markdown
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify
from utils import parsewords

# make sure this list of variables is up-to-date (i.e. matches
# the fields in the Software object
editables=('version','authors',
        'contact', 'description', 'project_url', 'tags', 'language',
        'os_license', 'tarball', 'screenshot', 'operating_systems',
        'paper_bib')

# don't change db of the following fields if they are empty
dontupdateifempty=['tarball', 'screenshot']

class Author(models.Model):
    name = models.CharField(maxlength=50, unique=True)
    slug = models.SlugField(editable=False)

    class Admin:
        pass

    def save(self):
        if not self.id:
            self.slug = slugify(self.name)
        super(Author,self).save()

    def get_absolute_url(self):
        return('mloss.software.views.list.software_by_author', (), { 'slug': self.slug })
    get_absolute_url = models.permalink(get_absolute_url)
    
    def __str__(self):
        return self.name
    

class Tag(models.Model):
    name = models.CharField(maxlength=50, unique=True)
    slug = models.SlugField(editable=False)

    class Admin:
        pass

    def save(self):
        if not self.id:
            self.slug = slugify(self.name)
        super(Tag,self).save()

    def get_absolute_url(self):
        return('mloss.software.views.list.software_by_tag', (), { 'slug': self.slug })
    get_absolute_url = models.permalink(get_absolute_url)
    
    def __str__(self):
        return self.name
    

class License(models.Model):
    name = models.CharField(maxlength=50, unique=True)
    slug = models.SlugField(editable=False)

    class Admin:
        pass

    def save(self):
        if not self.id:
            self.slug = slugify(self.name)
        super(License,self).save()

    def get_absolute_url(self):
        return('mloss.software.views.list.software_by_license', (), { 'slug': self.slug })
    get_absolute_url = models.permalink(get_absolute_url)
    
    def __str__(self):
        return self.name
    
class Language(models.Model):
    name = models.CharField(maxlength=50, unique=True)
    slug = models.SlugField(editable=False)

    class Admin:
        pass

    def save(self):
        if not self.id:
            self.slug = slugify(self.name)
        super(Language,self).save()

    def get_absolute_url(self):
        return('mloss.software.views.list.software_by_language', (), { 'slug': self.slug })
    get_absolute_url = models.permalink(get_absolute_url)
    
    def __str__(self):
        return self.name
    

class OpSys(models.Model):
    name = models.CharField(maxlength=50, unique=True)
    slug = models.SlugField(editable=False)

    class Admin:
        pass

    def save(self):
        if not self.id:
            self.slug = slugify(self.name)
        super(OpSys,self).save()

    def get_absolute_url(self):
        return('mloss.software.views.list.software_by_opsys', (), { 'slug': self.slug })
    get_absolute_url = models.permalink(get_absolute_url)
    
    def __str__(self):
        return self.name

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

    def get_by_author(self, slug):
        """
        Returns a QuerySet of Software submitted by a particular User.
        
        """
        return self.filter(authorlist__slug__exact=slug)

    def get_by_license(self, license):
        """
        Returns a QuerySet of Software sorted by a particular license.
        
        """
        return self.filter(licenselist__slug__exact=license)

    def get_by_language(self, language):
        """
        Returns a QuerySet of Software sorted by a particular language.
        
        """
        print language
        return self.filter(languagelist__slug__exact=language)

    def get_by_opsys(self, opsys):
        """
        Returns a QuerySet of Software sorted by a particular language.
        
        """
        return self.filter(opsyslist__slug__exact=opsys)

    def get_by_tag(self, tag):
        """
        Returns a QuerySet of Software sorted by a particular language.
        
        """
        return self.filter(taglist__slug__exact=tag)

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
    authorlist = models.ManyToManyField(Author, editable=False)
    contact = models.EmailField(max_length=80)
    description = models.TextField()
    description_html = models.TextField(editable=False)
    project_url = models.URLField(verify_exists=False)
    jmlr_mloss_url = models.URLField(verify_exists=False, blank=True)
    tags = models.CharField(max_length=200,blank=True)
    taglist = models.ManyToManyField(Tag, editable=False)
    language = models.CharField(max_length=200,blank=True)
    languagelist = models.ManyToManyField(Language, editable=False)
    os_license = models.CharField(max_length=200)
    licenselist = models.ManyToManyField(License, editable=False)
    operating_systems = models.CharField(max_length=200)
    opsyslist = models.ManyToManyField(OpSys, editable=False)
    paper_bib = models.TextField(blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()
    tarball = models.FileField(upload_to="code_archive/",blank=True,null=True)

    average_features_rating = models.FloatField(editable=False, blank=True, null=True)
    average_usability_rating = models.FloatField(editable=False, blank=True, null=True)
    average_documentation_rating = models.FloatField(editable=False, blank=True, null=True)
    total_number_of_votes = models.IntegerField(editable=False, blank=True, null=True)

    total_number_of_views = models.IntegerField(editable=False, blank=True, null=True)
    total_number_of_downloads = models.IntegerField(editable=False, blank=True, null=True)

    try:
        from PIL import Image  
        screenshot = models.ImageField(upload_to="screenshot_archive/",blank=True,null=True)
    except ImportError:
        screenshot = models.FileField(upload_to="screenshot_archive/",blank=True,null=True)
       

    objects = SoftwareManager()

    def get(self, a, b):
        return self.__dict__[a]

    def update_list(self,listname,objname,fieldname):
        current = eval('self.'+listname+'.all()')
        newlist = parsewords(self,fieldname=fieldname)

        # clear out old items
        for item in current:
            if item.name not in newlist:
                eval('self.'+listname+'.remove(item)')

        # add new items
        for item_name in newlist:
            if item_name not in [item.name for item in current]:
                try:
                    item = eval(objname+'.objects.get(name=\''+item_name+'\')')
                except eval(objname+'.DoesNotExist'):
                    item = eval(objname+'(name=\''+item_name+'\')')
                    item.save()
                eval('self.'+listname+'.add(item)')

    def save(self, auto_update_date=True):
        if not self.id:
            self.pub_date = datetime.datetime.now()
        if auto_update_date:
            self.updated_date = datetime.datetime.now()
        if not self.total_number_of_downloads:
            self.total_number_of_downloads=0
        if not self.total_number_of_views:
            self.total_number_of_views=0

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

        # Update authorlist, taglist, licenselist, langaugelist, opsyslist
        self.update_list('authorlist','Author','authors')
        self.update_list('taglist','Tag','tags')
        self.update_list('licenselist','License','os_license')
        self.update_list('languagelist','Language','language')
        self.update_list('opsyslist','OpSys','operating_systems')

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

    def get_stats_for_today(self):
        t = datetime.date.today().strftime("%Y-%m-%d")
        stats, flag = SoftwareStatistics.objects.get_or_create(software=self, date=t)
        return stats

    def update_views(self):
        if self.total_number_of_views:
            self.total_number_of_views += 1
        else:
            self.total_number_of_views = 1

        self.save(auto_update_date=False)
        e=self.get_stats_for_today()
        e.update_views()

    def update_downloads(self):
        if self.total_number_of_downloads:
            self.total_number_of_downloads += 1
        else:
            self.total_number_of_downloads = 1

        self.save(auto_update_date=False)
        e=self.get_stats_for_today()
        e.update_downloads()
        
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
        list_display = ('software', 'user', 'features', 'usability', 'documentation')
        pass

class SoftwareStatistics(models.Model):
    """
    Statistics about a software project
    """
    software = models.ForeignKey(Software)
    date = models.DateField()
    number_of_views = models.IntegerField(default=0)
    number_of_downloads = models.IntegerField(default=0)

    def update_views(self):
        self.number_of_views += 1
        self.save()

    def update_downloads(self):
        self.number_of_downloads += 1
        self.save()
    
    class Admin:
        list_display = ('date', 'number_of_views', 'number_of_downloads')
        pass
