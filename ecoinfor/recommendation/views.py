from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from .models import RecomandStock
from .stock_data import sina_latest_data
from .stock_name_code import name_code
from .index_data import latest_index_data

def index(request):
	template = loader.get_template('recommendation/index.html')
	index_list = []
	stock_list = ['000001', '399001', '395004', '399005']
	index_dict = latest_index_data(stock_list)
	for key in stock_list:
		index_list.append(index_dict[key]['open'])
	stockcode_class = RecomandStock.objects.order_by('-time')[:10]
	stockcode_list = []
	for key in stockcode_class:
		stockcode_list.append(key.stockcode)
	stock_dict = sina_latest_data(stockcode_list)
	stock_keys = stock_dict.keys()
	stock_list = []
	name = name_code()
	for key in stock_keys:
		if key not in name.keys():
			stock_dict[key]['chi_name'] = 'null'
		else:
			stock_dict[key]['chi_name'] = name[key]
	stock_list_original = stock_dict.values()
	for stock in stock_list_original:
		if stock['chi_name'] == 'null':
			continue
		stock_list.append((stock['chi_name'], stock['open'], stock['yes_close'], stock['cur_price'], stock['high'], stock['low'], stock['vol']))

	context = {
		'stock_list': stock_list, 'szzs': index_list[0], 'shenz': index_list[1], 'cyb': index_list[2], 'zxb': index_list[3]
	}
	return HttpResponse(template.render(context, request))

def detail_news(request, news_id):
	try:
		news = News.objects.get(pk = news_id)
	except News.DoesNotExist:
		raise Http404("No more news. Please try again later.")
	return render(request, 'mainpage/detail.html', {'news':news})