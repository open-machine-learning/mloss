import math
 
from django.template import Library, Node, TemplateSyntaxError, VariableDoesNotExist, resolve_variable
from django.conf import settings
 
register = Library()
 
IMG_TEMPLATE = '<img src="%s" alt="%s"/>'
 
PATH_TO_WHOLE_STAR = IMG_TEMPLATE % (settings.MEDIA_URL + 'images/stars/star.png', "Whole Star")
PATH_TO_THREE_QUARTER_STAR = IMG_TEMPLATE % (settings.MEDIA_URL + 'images/stars/three-quarter.png', "3/4 Star")
PATH_TO_HALF_STAR = IMG_TEMPLATE % (settings.MEDIA_URL + 'images/stars/half.png', "1/2 Star")
PATH_TO_QUARTER_STAR = IMG_TEMPLATE % (settings.MEDIA_URL + 'images/stars/quarter.png', "1/4 Star")
PATH_TO_BLANK_STAR = IMG_TEMPLATE % (settings.MEDIA_URL + 'images/stars/blank.png', "Empty Star")
 
class ShowStarsNode(Node):
    """ Default rounding is to the whole unit """
    def __init__(self, context_var, total_stars, round_to):
        self.context_var = context_var
        self.total_stars = int(total_stars)
        self.round_to = round_to.lower()
 
    def render(self, context):
        try:
            stars = resolve_variable(self.context_var, context)
        except VariableDoesNotExist:
            return ''
 
        if self.round_to == "half":
            stars = round(stars*2)/2
        elif self.round_to == "quarter":
            stars = round(stars*4)/4
        else:
            stars = round(stars)
 
        fraction, integer = math.modf(stars)
        integer = int(integer)
        output = []
 
        for whole_star in range(integer):
            output.append(PATH_TO_WHOLE_STAR)
        if self.round_to == 'half' and fraction == .5:
            output.append(PATH_TO_HALF_STAR)
        elif self.round_to == 'quarter':
            if fraction == .25:
                output.append(PATH_TO_QUARTER_STAR)
            elif fraction == .5:
                output.append(PATH_TO_HALF_STAR)
            elif fraction == .75:
                output.append(PATH_TO_THREE_QUARTER_STAR)
 
        if fraction:
            integer += 1
 
        blanks = int(self.total_stars - integer)
 
        for blank_star in range(blanks):
            output.append(PATH_TO_BLANK_STAR)
 
        return "".join(output)
 
""" show_stars context_var of 5 round to half """
def do_show_stars(parser, token):
    args = token.contents.split()
    if len(args) != 7:
        raise TemplateSyntaxError('%s tag requires exactly six arguments' % args[0])
    if args[2] != 'of':
        raise TemplateSyntaxError("second argument to '%s' tag must be 'of'" % args[0])
    if args[4] != 'round':
        raise TemplateSyntaxError("fourth argument to '%s' tag must be 'round'" % args[0])
    if args[5] != 'to':
        raise TemplateSyntaxError("fourth argument to '%s' tag must be 'to'" % args[0])
    return ShowStarsNode(args[1], args[3], args[6])   
 
register.tag('show_stars', do_show_stars)
