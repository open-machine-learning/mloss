from django.contrib.syndication.views import Feed
from aggregator.models import FeedItem

class CommunityAggregatorFeed(Feed):
    title = "The mloss.org community aggregator"
    link = "http://mloss.org"
    description = "Aggregated feeds from the machine learning community."

    def items(self):
        return FeedItem.objects.all()[:10]
