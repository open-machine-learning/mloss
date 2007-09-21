# Create your views here.
from django.shortcuts import render_to_response
from forshow.models import News
from forshow.models import Faq

def newsindex(request):
    """
    List of all news items
    """
    all_news_items = News.objects.all().order_by('-publication_date')
    return render_to_response('news_index.html',
                              {'all_news_items': all_news_items},)


def faqindex(request):
    """
    List of all FAQ items
    """
    all_faq_items = Faq.objects.all()
    return render_to_response('faq_index.html',
                              {'all_faq_items': all_faq_items},)
