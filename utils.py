import re
from django.template.defaultfilters import stringfilter
from django.core.mail import send_mail
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
            # only send out things once every 60 seconds 
            if now-s.last_updated > datetime.timedelta(0, 60):
                #print subject
                #print s.user.email
                #print message
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [ s.user.email ],fail_silently=True)
                s.last_updated=now
                s.save()
