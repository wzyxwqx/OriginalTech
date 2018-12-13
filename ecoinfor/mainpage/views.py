from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.db import connection
from django.views import generic

from .models import Message, Share, Market
# Create your views here.


class IndexView(generic.ListView):
    template_name = 'mainpage/index.html'
    context_object_name = 'latest_message_list'

    def get_queryset(self):
        """Return the last ten published messages"""
        return Message.objects.order_by('-pub_date')[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_markets'] = list(Market.objects.all())
        return context


def index(request):
	template = loader.get_template('mainpage/index.html')
	# latest_message_list = Message.objects.order_by('-pub_date')[:10]

	cursor = connection.cursor()
	sql = "SELECT * from cs_news WHERE keystock != '' ORDER BY time limit 10"
	cursor.execute(sql)
	
	results = cursor.fetchall()
	latest_news_list = []
	for key in results:
		latest_news_list.append(key[1])

	context = {
		'latest_news_list': latest_news_list,
	}
	return HttpResponse(template.render(context, request))


def detail_share(request, share_id):
	try:
		share = Share.objects.get(pk = message_id)
	except Share.DoesNotExist:
		raise Http404("This share does not exist. Please try again later.")
	return render(request, 'share/detail.html', {'share':share})


"""def consultant(request):
	template = loader.get_template('consultant/index.html')
	latest_share_list = Share.objects.order_by('-hot_index')[:10]
	context = {
		'latest_share_list': latest_share_list
	}
	return HttpResponse(template.render(context, request))"""


def detail_message(request, message_id):
	try:
		message = Message.objects.get(pk = message_id)
	except Message.DoesNotExist:
		raise Http404("Message does not exist. Please try again later.")
	return render(request, 'mainpage/detail.html', {'message':message})
