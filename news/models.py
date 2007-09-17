from django.db import models
from software.models import Author

# Create your models here.
class News(models.Model):
    headline = models.CharField(maxlength=200)
    author = models.OneToOneField(Author)
    publication_date = models.DateField()
    article = models.TextField()

    class Meta:
        ordering = ('-publication_date',)
    class Admin:
        fields = (
            ('Metadata', {'fields': ('headline','publication_date')}),
            ('None', {'fields': ('headline','author','publication_date','article')}),
            )
        
    def __str__(self):
        return self.headline
    
