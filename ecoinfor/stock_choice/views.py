from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.db import connection, models
from django.views import generic
from django.utils import timezone

from .models import Stock

# Create your views here.
def index(request):
	template = loader.get_template('stock_choice/index.html')

	"""
	cursor = connection.cursor()
	sql = "SELECT * from stock ORDER BY stockcode DESC limit 10"
	cursor.execute(sql)

	# In results every stock contain three properties: id, name, another id called stockcode.
	results = cursor.fetchall()
	
	
	latest_stock_list = []
	for key in results:
		latest_stock_list.append((key[0],key[1]))"""
	stk = Stock.objects.get(id = 10605)
	latest_stock_list = [stk]
	context = {
		'latest_stock_list': latest_stock_list,
	}
	return HttpResponse(template.render(context, request))


def detail_stock(request, stock_id):
	try:
		stk = Stock.objects.get(id = stock_id)
	except stk.DoesNotExist:
		raise Http404("This stock does not exist. Please try again later.")
	return render(request, 'stock_choice/detail.html', {'stk':stk})


# The page of the Consultant, still on construction
"""
def consultant(request):
	template = loader.get_template('consultant/index.html')
	latest_stock_list = stock.objects.order_by('-hot_index')[:10]
	context = {
		'latest_stock_list': latest_stock_list
	}
	return HttpResponse(template.render(context, request))"""