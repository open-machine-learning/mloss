from django.db import models
from utils import slugify

class BlogItem(models.Model):
    pub_date = models.DateTimeField()
    slug = models.SlugField(unique_for_date='pub_date', editable=True)
    headline = models.CharField(max_length=200)
    summary = models.TextField(help_text="Use markdown.")
    body = models.TextField(help_text="Use markdown.")
    author = models.CharField(max_length=100)

    class Meta:
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'

    def __unicode__(self):
        return unicode(self.headline)

    def get_absolute_url(self):
        return "/community/blog/%s/%s/" % (self.pub_date.strftime("%Y/%b/%d").lower(), self.slug)

    def get_comment_url(self):
        return "/community/blog/%s/%s/#comments" % (self.pub_date.strftime("%Y/%b/%d").lower(), self.slug)

    def save(self):
        if not self.id:
            self.slug = slugify(self.headline)
        super(BlogItem,self).save()
