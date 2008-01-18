from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import rfc2822_date, SyndicationFeed
from django.utils.xmlutils import SimplerXMLGenerator

class WellFormedWebRss(SyndicationFeed):
    mime_type = 'application/rss+xml'
    def write(self, outfile, encoding):
        handler = SimplerXMLGenerator(outfile, encoding)
        handler.startDocument()
        handler.startElement(u"rss", {u"version": self._version, u"xmlns:wfw": u"http://wellformedweb.org/CommentAPI/"})
        handler.startElement(u"channel", {})
        handler.addQuickElement(u"title", self.feed['title'])
        handler.addQuickElement(u"link", self.feed['link'])
        handler.addQuickElement(u"description", self.feed['description'])
        if self.feed['language'] is not None:
            handler.addQuickElement(u"language", self.feed['language'])
        for cat in self.feed['categories']:
            handler.addQuickElement(u"category", cat)
        if self.feed['feed_copyright'] is not None:
            handler.addQuickElement(u"copyright", self.feed['feed_copyright'])
        handler.addQuickElement(u"lastBuildDate", rfc2822_date(self.latest_post_date()).decode('ascii'))
        self.write_items(handler)
        self.endChannelElement(handler)
        handler.endElement(u"rss")

    def endChannelElement(self, handler):
        handler.endElement(u"channel")

    _version = u"2.0"
    def write_items(self, handler):
        for item in self.items:
            handler.startElement(u"item", {})
            handler.addQuickElement(u"title", item['title'])
            handler.addQuickElement(u"link", item['link'])
            if item['description'] is not None:
                handler.addQuickElement(u"description", item['description'])

            # Author information.
            if item["author_name"] and item["author_email"]:
                handler.addQuickElement(u"author", "%s (%s)" % \
                    (item['author_email'], item['author_name']))
            elif item["author_email"]:
                handler.addQuickElement(u"author", item["author_email"])
            elif item["author_name"]:
                handler.addQuickElement(u"dc:creator", item["author_name"], {"xmlns:dc": u"http://purl.org/dc/elements/1.1/"})

            if item['pubdate'] is not None:
                handler.addQuickElement(u"pubDate", rfc2822_date(item['pubdate']).decode('ascii'))
            if item['comments'] is not None:
                handler.addQuickElement(u"comments", item['comments'])
            if item.has_key('wfw_commentRss') and item['wfw_commentRss'] is not None:
                handler.addQuickElement(u"wfw:commentRss", item['wfw_commentRss'])
            if item['unique_id'] is not None:
                handler.addQuickElement(u"guid", item['unique_id'])

            # Enclosure.
            if item['enclosure'] is not None:
                handler.addQuickElement(u"enclosure", '',
                    {u"url": item['enclosure'].url, u"length": item['enclosure'].length,
                        u"type": item['enclosure'].mime_type})

            # Categories.
            for cat in item['categories']:
                handler.addQuickElement(u"category", cat)

            handler.endElement(u"item")

    def add_commentRss(self, c):
        self.items[-1]['wfw_commentRss']=c
