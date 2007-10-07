from django.db import models
from software import managers
import datetime
from markdown import markdown
from django.utils.html import strip_tags

# Create your models here.
class Software(models.Model):
    """
    A description of some machine learning open source
    software project.
    """
    screenshot = models.ImageField(upload_to="media/screenshot_archive/",blank=True,null=True)
    title = models.CharField(max_length=80)
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
    tarball = models.FileField(upload_to="media/code_archive/",blank=True,null=True)

    def save(self):
        if not self.id:
            self.pub_date = datetime.datetime.now()
        self.updated_date = datetime.datetime.now()

        # Use safe_mode in Markdown to prevent arbitrary input
        # and strip all html tags from CharFields
        self.title = strip_tags(self.title)
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
            'fields': ('title', 'authors')}),
            ('None', {
            'fields': ('description', 'project_url', 'tags', 'language', 'os_license', 'pub_date', 'updated_date')}),
            )
        list_filter = ['pub_date']
        date_hierarchy = 'pub_date'
        search_fields = ['title']

    class Meta:
        ordering = ('-pub_date',)

