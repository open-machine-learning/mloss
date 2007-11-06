import re
from django.template.defaultfilters import stringfilter

# not quite sure where to put this code
def parsewords(curobj,fieldname='language'):
    """
    Returns a set of words contained in fieldname
    """
    DELIMITERS = '(,|and)'
    STOPWORDS = set(['',',','and'])
    
    unique_words = list()
    curstr = eval('curobj.'+fieldname)
    curwords = re.split(DELIMITERS,curstr)
    for word in curwords:
        cleanword = word.strip().lower()
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
    value = unicode(re.sub('[^\w\s-+]', '', value).strip().lower())
    return re.sub('[-+\s]+', '-', value)
slugify = stringfilter(slugify)

