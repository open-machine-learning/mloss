from django.contrib.syndication.feeds import Feed
from blog.models import BlogItem
import datetime

class WeblogEntryFeed(Feed):
    title = "The mloss weblog"
    link = "http://mloss.org/weblog"
    description = "Some thoughts about machine learning open source software"

    def items(self):
        return BlogItem.objects.filter(pub_date__lte=datetime.datetime.now())[:10]
