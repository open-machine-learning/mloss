from django.db import models
from software import managers
import datetime
from markdown import markdown
from django.utils.html import strip_tags
from django.contrib.auth.models import User

# make sure this list of variables is up-to-date (i.e. matches
# the fields in the Software object
editables=('title','version','authors',
        'contact', 'description', 'project_url', 'tags', 'language',
        'os_license', 'tarball', 'screenshot' )

# don't change db of the following fields if they are empty
dontupdateifempty=['tarball', 'screenshot']

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
    tags = models.CharField(max_length=200,blank=True)
    language = models.CharField(max_length=200,blank=True)
    os_license = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    tarball = models.FileField(upload_to="code_archive/",blank=True,null=True)
    screenshot = models.ImageField(upload_to="screenshot_archive/",blank=True,null=True)

    def get(self, a, b):
        return self.__dict__[a]

    def save(self):
        if not self.id:
            self.pub_date = datetime.datetime.now()
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
        super(Software, self).save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return ('software.views.entry.software_detail', (), { 'software_id': str(self.id) })

    get_absolute_url = models.permalink(get_absolute_url)

    class Admin:
        fields = (
            ('Metadata', {
            'fields': ('title', 'version', 'authors')}),
            ('None', {
            'fields': ('user', 'description', 'project_url', 'tags', 'language',
				'os_license', 'pub_date', 'updated_date', 'tarball', 'screenshot')}),
            )
        list_filter = ['pub_date']
        date_hierarchy = 'pub_date'
        search_fields = ['title']

    class Meta:
        ordering = ('-pub_date',)

