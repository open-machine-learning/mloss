import re
from django.template.defaultfilters import stringfilter
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.contrib.comments.signals import comment_will_be_posted
import settings
import datetime

# not quite sure where to put this code
def parsewords(curobj,fieldname='language'):
    """
    Returns a set of words contained in fieldname
    """
    DELIMITERS = u'(,| and |et\.?al\.?)'
    STOPWORDS = set(['',',','and','et.al.','et.al','etal','others'])
    STRIPLIST = ('.',',')
    
    unique_words = list()
    curstr = unicode(eval('curobj.'+fieldname))
    curstr = curstr.lower()
    curwords = re.split(DELIMITERS,curstr)
    for word in curwords:
        cleanword = word.strip()
        while cleanword.startswith(STRIPLIST) or cleanword.endswith(STRIPLIST):
            for stripchar in STRIPLIST:
                cleanword = cleanword.strip(stripchar)
        if (cleanword not in unique_words) and (cleanword not in STOPWORDS):
            unique_words.append(cleanword)

    unique_words.sort()
    return unique_words

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha chars and
    converts spaces to hyphens.
    """
    import unicodedata
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s\-\+]', '', value).strip().lower())
    return re.sub('[\-\+\s]+', '-', value)
slugify = stringfilter(slugify)


def send_mails(subscribers, subject, message):
    # we don't use send_mass_mail as we don't want to leak other users email addresses
    for s in subscribers:
        if not s.bookmark:
            now=datetime.datetime.now()
            # only send out things once every 600 seconds 
            if now-s.last_updated > datetime.timedelta(0, 600):
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [ s.user.email ],fail_silently=True)
                s.last_updated=now
                s.save()

def comment_spam_test(**kwargs):
    """
         instance is the comment object
    """

    blacklist_identical=['', 'Nice article','Wow! Thank you! I always wanted to write in my blog something like that. Can I take part of your post to my site? Of course, I will add backlink?']
    blacklist_contains=['[/URL]',
			'http://www.internet-poker.de',
			'http://www.vanessa-sucht.com/',
			'http://www.planetresource.net',
			'http://www.organic-farming.org',
			'http://100-free-web-host.com',
			'naked girls',
			'organic farming',
			'easiest ways to earn money',
			'principal-nude',
			'hot brunette',
			'earn money online',
			'adult-friend-finder',
			'Hi, interesting post. I have been pondering this issue,so thanks for sharing. I will definitely be subscribing to your blog.',
			'Hello. And Bye.',
			'http://quick-ways-to-earn-extra-cash.blogspot.com/'
			'earn money online',
			'http://www.mydatelove.com',
			'best buy and loss weight',
			]

    comment=kwargs['comment'].comment
    request=kwargs['request']

    if not request.user.is_authenticated():
        return False

    if not comment or comment in blacklist_identical:
        return False

    for b in blacklist_contains:
        if comment.find(b)!=-1:
            return False

    if strip_tags(comment) != comment:
        return False

    return True;

comment_will_be_posted.connect(comment_spam_test)
