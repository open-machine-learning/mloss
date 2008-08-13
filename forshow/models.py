from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.
class News(models.Model):
    headline = models.CharField(max_length=200)
    author = models.ManyToManyField(User)
    publication_date = models.DateField()
    article = models.TextField()

    class Meta:
        ordering = ('-publication_date',)

class NewsAdmin(admin.ModelAdmin):
    list_display = ('headline', 'publication_date')

class Faq(models.Model):
    question = models.TextField()
    answer = models.TextField()

class FaqAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')
    fieldsets = (
            (None, {'fields': ('question','answer')}),
            )


admin.site.register(News, NewsAdmin)
admin.site.register(Faq, FaqAdmin)
