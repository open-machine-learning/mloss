from django import template
import random

register = template.Library()

class Permutator(template.Node):
    def __init__(self, context_var):
        self.context_var = context_var

    def render(self, context):
        return self.context_var

def permute_items(parser, token):
    items = token.contents[13:].split('|')
    random.shuffle(items)
    return Permutator(", ".join(items))

register.tag('permute_items', permute_items)
