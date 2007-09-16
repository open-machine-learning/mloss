from django.db import models
from software import managers

# Create your models here.
class Author(models.Model):
    salutation = models.CharField(maxlength=10)
    first_name = models.CharField(maxlength=100)
    last_name = models.CharField(maxlength=100)
    email = models.EmailField()

    class Admin:
        pass

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)
    
class Software(models.Model):
	title = models.CharField(maxlength=100)
	authors = models.ManyToManyField(Author)
	description = models.TextField(maxlength=1000)
	project_url = models.URLField(verify_exists=False) 
	pub_date = models.DateTimeField()
	updated_date = models.DateTimeField()


	objects = managers.SoftwareManager()

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
		return ('software.views.entry.snippet_detail', (), { 'snippet_id': str(self.id) })
	get_absolute_url = models.permalink(get_absolute_url)
