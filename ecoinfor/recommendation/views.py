from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from .models import News
# Create your views here.

def index(request):
	template = loader.get_template('recommendation/index.html')
	latest_news_list = News.objects.order_by('-pub_date')[:10]
	context = {
		'latest_news_list': latest_news_list,
	}
	return HttpResponse(template.render(context, request))

def detail_news(request, news_id):
	try:
		news = News.objects.get(pk = news_id)
	except News.DoesNotExist:
		raise Http404("No more news. Please try again later.")
	return render(request, 'mainpage/detail.html', {'news':news})