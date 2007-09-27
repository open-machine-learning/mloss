from django.db import models
from software.models import Author

# Create your models here.
class News(models.Model):
    headline = models.CharField(maxlength=200)
    author = models.ManyToManyField(Author)
    publication_date = models.DateField()
    article = models.TextField()

    class Meta:
        ordering = ('-publication_date',)
    class Admin:
        list_display = ('headline', 'publication_date')
    
class Faq(models.Model):
    question = models.TextField()
    answer = models.TextField()

    class Admin:
        list_display = ('question', 'answer')
