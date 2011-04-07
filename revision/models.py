import datetime
from django.utils.html import strip_tags
from django.db import models
from django.db.models import Q

from software.models import Software
from markdown import markdown
from utils import parsewords, slugify, slugify_uniquely

# make sure these lists of variables are up-to-date (i.e. match
# the fields in the Software object
editables=('version','authors',
        'contact', 'short_description', 'description', 'project_url', 'tags', 'language',
        'os_license', 'tarball', 'download_url', 'screenshot', 'thumbnail',
        'operating_systems', 'dataformats', 'paper_bib', 'changes')

#'authorlist', 'taglist', 'languagelist', 'licenselist', 'opsyslist', 
# don't change db of the following fields if they are empty
dontupdateifempty=['tarball', 'screenshot', 'thumbnail']

class Author(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(editable=False)

    def save(self, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Author,self).save(kwargs)

    def get_absolute_url(self):
        return('mloss.software.views.list.software_by_author', (), { 'slug': self.slug })
    get_absolute_url = models.permalink(get_absolute_url)

    def __unicode__(self):
        return unicode(self.name)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(editable=False)

    def save(self, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Tag,self).save(kwargs)

    def get_absolute_url(self):
        return('mloss.software.views.list.software_by_tag', (), { 'slug': self.slug })
    get_absolute_url = models.permalink(get_absolute_url)

    def __unicode__(self):
        return unicode(self.name)

class License(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(editable=False)

    def save(self, **kwargs):
        if not self.id:
            self.slug = slugify_uniquely(self.name)
        super(License,self).save(kwargs)

    def get_absolute_url(self):
        return('mloss.software.views.list.software_by_license', (), { 'slug': self.slug })
    get_absolute_url = models.permalink(get_absolute_url)

    def __unicode__(self):
        return unicode(self.name)

class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(editable=False)

    def save(self, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Language,self).save(kwargs)

    def get_absolute_url(self):
        return('mloss.software.views.list.software_by_language', (), { 'slug': self.slug })
    get_absolute_url = models.permalink(get_absolute_url)

    def __unicode__(self):
        return unicode(self.name)

class OpSys(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(editable=False)

    def save(self, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(OpSys,self).save(kwargs)

    def get_absolute_url(self):
        return('mloss.software.views.list.software_by_opsys', (), { 'slug': self.slug })
    get_absolute_url = models.permalink(get_absolute_url)

    def __unicode__(self):
        return unicode(self.name)

class DataFormat(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(editable=False)

    def save(self, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(DataFormat,self).save(kwargs)

    def get_absolute_url(self):
        return('mloss.software.views.list.software_by_dataformat', (), { 'slug': self.slug })
    get_absolute_url = models.permalink(get_absolute_url)

    def __unicode__(self):
        return unicode(self.name)

class RevisionManager(models.Manager):
    def get_jmlr(self):
        """
        Returns a QuerySet of Software published in jmlr

        """
        return self.filter(revision=0, jmlr_mloss_url__startswith='http://')

    def get_by_submitter(self, username):
        """
        Returns a QuerySet of Software submitted by a particular User.

        """
        return self.filter(revision=0, software__user__username__exact=username)

    def get_by_author(self, slug):
        """
        Returns a QuerySet of Software submitted by a particular User.

        """
        return self.filter(revision=0, authorlist__slug__exact=slug)

    def get_by_license(self, license):
        """
        Returns a QuerySet of Software sorted by a particular license.

        """
        return self.filter(revision=0, licenselist__slug__exact=license)

    def get_by_language(self, language):
        """
        Returns a QuerySet of Software sorted by a particular language.

        """
        return self.filter(revision=0, languagelist__slug__exact=language)

    def get_by_opsys(self, opsys):
        """
        Returns a QuerySet of Software sorted by a particular language.

        """
        return self.filter(revision=0, opsyslist__slug__exact=opsys)

    def get_by_dataformat(self, dataformat):
        """
        Returns a QuerySet of Software sorted by a particular language.

        """
        return self.filter(revision=0, dataformatlist__slug__exact=dataformat)

    def get_by_tag(self, tag):
        """
        Returns a QuerySet of Software sorted by a particular language.

        """
        return self.filter(revision=0, taglist__slug__exact=tag)

    def get_by_searchterm(self, searchterm):
        """
        Returns a QuerySet of Software matching the searchterm

        """
        return self.filter(revision=0).filter(
                Q(software__user__username__icontains=searchterm) |
                Q(software__title__icontains=searchterm) |
                Q(version__icontains=searchterm) |
                Q(authors__icontains=searchterm) |
                Q(description__icontains=searchterm) |
                Q(tags__icontains=searchterm) |
                Q(language__icontains=searchterm) |
                Q(operating_systems__icontains=searchterm) |
                Q(os_license__icontains=searchterm))



# Create your models here.
class Revision(models.Model):
    """
    A description of some machine learning open source
    software project.
    """
    software = models.ForeignKey(Software)
    version = models.CharField(max_length=80)
    authors = models.CharField(max_length=200)
    authorlist = models.ManyToManyField(Author, editable=False)
    contact = models.EmailField(max_length=80)
    short_description = models.TextField()
    description = models.TextField()
    description_html = models.TextField(editable=False)
    changes = models.TextField()
    changes_html = models.TextField(editable=False)
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
    dataformats = models.CharField(max_length=200)
    dataformatlist = models.ManyToManyField(DataFormat, editable=False)
    paper_bib = models.TextField(blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    download_url = models.URLField(verify_exists=False, blank=True, null=True)
    tarball = models.FileField(upload_to="code_archive/",blank=True,null=True)

    # revision number, where 0 means latest
    revision = models.IntegerField(default=0)

    objects = RevisionManager()

    try:
        from PIL import Image  
        screenshot = models.ImageField(upload_to="screenshot_archive/",blank=True,null=True)
        thumbnail = models.ImageField(upload_to="thumbnail_archive/",blank=True,null=True)
    except ImportError:
        screenshot = models.FileField(upload_to="screenshot_archive/",blank=True,null=True)
        thumbnail = models.FileField(upload_to="thumbnail_archive/",blank=True,null=True)

    def is_downloadable(self):
        return self.tarball or self.download_url

    def get(self, a, b):
        if a in self.__dict__:
            return self.__dict__[a]
        elif a == 'title':
            return self.software.title
        elif a == 'user':
            return self.software.user

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

    def save(self, **kwargs):
        new_revision = not self.id
        silent_update =  kwargs.has_key('silent_update')
        if silent_update:
            kwargs.pop('silent_update')
        if new_revision and self.pub_date is None:
            self.pub_date = datetime.datetime.now()
        if not silent_update:
            self.updated_date = datetime.datetime.now()

        # Use safe_mode in Markdown to prevent arbitrary input
        # and strip all html tags from CharFields
        self.version = strip_tags(self.version)
        self.authors = strip_tags(self.authors)
        self.changes_html = markdown(self.changes, safe_mode=True)
        self.description_html = markdown(self.description, safe_mode=True)
        self.tags = strip_tags(self.tags)
        self.language = strip_tags(self.language)
        self.os_license = strip_tags(self.os_license)
        self.paper_bib = strip_tags(self.paper_bib)
        self.operating_systems = strip_tags(self.operating_systems)
        self.dataformats = strip_tags(self.dataformats)
        super(Revision, self).save(kwargs)

        # Update authorlist, taglist, licenselist, langaugelist, opsyslist
        self.update_list('authorlist','Author','authors')
        self.update_list('taglist','Tag','tags')
        self.update_list('licenselist','License','os_license')
        self.update_list('languagelist','Language','language')
        self.update_list('opsyslist','OpSys','operating_systems')
        self.update_list('dataformatlist','DataFormat','dataformats')

        # send out notifications on updates
        if not silent_update:
            self.software.notify_update()

    def get_authorlist(self):
        return [ x for x in self.authorlist.all() ]
    def get_taglist(self):
        return [ x for x in self.taglist.all() ]
    def get_licenselist(self):
        return [ x for x in self.licenselist.all() ]
    def get_languagelist(self):
        return [ x for x in self.languagelist.all() ]
    def get_opsyslist(self):
        return [ x for x in self.opsyslist.all() ]
    def get_dataformatlist(self):
        return [ x for x in self.dataformatlist.all() ]

    def get_description_page(self):
        s="<html>" + self.description_html + "</html>"
        return s.encode('utf-8')

    def __unicode__(self):
        return unicode(self.software.title)

    def get_absolute_url(self):
        return('revision.views.revision_detail', [str(self.id)])
    get_absolute_url = models.permalink(get_absolute_url)

    def get_absolute_homepage_url(self):
        return('revision.views.view_homepage', [str(self.id)])
    get_absolute_homepage_url = models.permalink(get_absolute_homepage_url)

    def get_absolute_jmlr_homepage_url(self):
        return('revision.views.view_jmlr_homepage', [str(self.id)])
    get_absolute_jmlr_homepage_url = models.permalink(get_absolute_jmlr_homepage_url)

    def get_absolute_download_url(self):
        return('revision.views.download_revision', [str(self.id)])
    get_absolute_download_url = models.permalink(get_absolute_download_url)

    def get_absolute_bib_url(self):
        return('revision.views.get_bibitem', [str(self.id)])
    get_absolute_bib_url = models.permalink(get_absolute_bib_url)

    def get_absolute_paperbib_url(self):
        return('revision.views.get_paperbibitem', [str(self.id)])
    get_absolute_paperbib_url = models.permalink(get_absolute_paperbib_url)

    class Meta:
        ordering = ('-pub_date',)

def clean_list(objname,fieldname):
    curlist = []
    allsoft = Revision.objects.all()
    for cursoft in allsoft:
        tlist = parsewords(cursoft,fieldname)
        for item in tlist:
            curlist.append(item)

    oldlist = eval(objname+'.objects.all()')
    for item in oldlist:
        if item.name not in curlist:
            item.delete()

def clean_all():
    clean_list('Author','authors')
    clean_list('Tag','tags')
    clean_list('License','os_license')
    clean_list('Language','language')
    clean_list('OpSys','operating_systems')
    clean_list('DataFormat','dataformats')
