from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class News(models.Model):
    headline = models.CharField(max_length=200)
    author = models.ManyToManyField(User)
    publication_date = models.DateField()
    article = models.TextField()

    class Meta:
        ordering = ('-publication_date',)

class Faq(models.Model):
    question = models.TextField()
    answer = models.TextField()

