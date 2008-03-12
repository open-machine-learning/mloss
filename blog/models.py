from django.db import models

class BlogItem(models.Model):
    pub_date = models.DateTimeField()
    slug = models.SlugField(unique_for_date='pub_date')
    headline = models.CharField(maxlength=200)
    summary = models.TextField(help_text="Use raw HTML.")
    body = models.TextField(help_text="Use raw HTML.")
    author = models.CharField(maxlength=100)

    class Meta:
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'

    class Admin:
        list_display = ('pub_date', 'headline', 'author')

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        return "/community/blog/%s/%s/" % (self.pub_date.strftime("%Y/%b/%d").lower(), self.slug)
