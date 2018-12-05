from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse



from .models import Message, Share
# Create your views here.


def index(request):
	template = loader.get_template('mainpage/index.html')
	latest_message_list = Message.objects.order_by('-pub_date')[:10]
	context = {
		'latest_message_list': latest_message_list,

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







