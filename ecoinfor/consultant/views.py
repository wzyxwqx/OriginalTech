from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse


from .models import Share
# Create your views here.

def index(request):
	template = loader.get_template('consultant/index.html')
#	lastet_preference_list = Message.objects.order_by('-personal_index')
#	need change: using Personality.objects
	latest_share_list = Share.objects.order_by('-hot_index')[:10]
	context = {
		'latest_share_list': latest_share_list
	}
	return HttpResponse(template.render(context, request))

def detail_share(request, share_id):
	try:
		share = Share.objects.get(pk = share_id)
	except Share.DoesNotExist:
		raise Http404("This share does not exist. Please try again later.")
	return render(request, 'share/detail.html', {'share':share})