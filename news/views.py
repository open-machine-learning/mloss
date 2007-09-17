# Create your views here.
from django.shortcuts import render_to_response
from news.models import News

def index(request):
    """
    List of all news items
    """
    all_news_items = News.objects.all().order_by('-publication_date')
    return render_to_response('news/index.html',
                              {'all_news_items': all_news_items},)
