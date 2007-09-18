# Create your views here.
from django.shortcuts import render_to_response
from faq.models import Faq

def index(request):
    """
    List of all FAQ items
    """
    all_faq_items = Faq.objects.all()
    return render_to_response('faq/index.html',
                              {'all_faq_items': all_faq_items},)
