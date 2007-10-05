from django.db import models
from software import managers

# Create your models here.
class Software(models.Model):
    """
    A description of some machine learning open source
    software project.
    """
    title = models.CharField(max_length=80)
    authors = models.CharField(max_length=200)
    description = models.TextField()
    project_url = models.URLField(verify_exists=False)
    tags = models.CharField(max_length=200,blank=True)
    language = models.CharField(max_length=200,blank=True)
    os_license = models.CharField(max_length=200,blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    tarball = models.FileField(upload_to="media/code_archive/",blank=True)

    class Admin:
        fields = (
            ('Metadata', {
            'fields': ('title', 'authors')}),
            ('None', {
            'fields': ('description', 'project_url', 'pub_date', 'updated_date')}),
            )
        list_filter = ['pub_date']
        date_hierarchy = 'pub_date'
        search_fields = ['title']

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return ('software.views.entry.software_detail', (), { 'software_id': str(self.id) })
    get_absolute_url = models.permalink(get_absolute_url)
