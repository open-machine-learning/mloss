from django.db import models
from software import managers

# Create your models here.
class Author(models.Model):
    salutation = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    class Admin:
        pass

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Software(models.Model):
    """
    A description of some machine learning open source
    software project.
    """
    title = models.CharField(max_length=80)
    #authors = models.ManyToManyField(Author)
    authors = models.CharField(max_length=80)
    description = models.TextField()
    project_url = models.URLField(verify_exists=False)
    keyword1 = models.CharField(max_length=200,blank=True)
    keyword2 = models.CharField(max_length=200,blank=True)
    keyword3 = models.CharField(max_length=200,blank=True)
    keyword4 = models.CharField(max_length=200,blank=True)
    keyword5 = models.CharField(max_length=200,blank=True)
    language = models.CharField(max_length=200,blank=True)
    os_license = models.CharField(max_length=200,blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    tarball = models.FileField(upload_to="media/code_archive/",blank=True)

    #objects = managers.SoftwareManager()

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
