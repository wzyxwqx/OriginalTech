from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.db import connection
from django.views import generic
from .stock_name_code import name_code

from .index_data import latest_index_data
from .models import TempNews
# Create your views here.

def index(request):
    template = loader.get_template('mainpage/index.html')
    results = TempNews.objects.exclude(abstract='None').exclude(abstract='').values('title', 'time', 'abstract').distinct().order_by('-time')[:15]
    latest_news_list = []
    index_list = []
    stock_list = ['000001', '399001', '395004', '399005']
    index_dict = latest_index_data(stock_list)
    for key in stock_list:
        index_list.append(index_dict[key]['open'])
    for key in results:
        print(key)
        latest_news_list.append((key['title'], key['time'], key['abstract']))


    context = {
		'latest_news_list': latest_news_list, 'szzs': index_list[0], 'shenz': index_list[1], 'cyb': index_list[2], 'zxb': index_list[3]
	}
    return HttpResponse(template.render(context, request))

def content_index(request, title):
    res = name_code()
    template = loader.get_template('mainpage/content.html')
    results = TempNews.objects.exclude(abstract='None').exclude(abstract='').values('title', 'time', 'content', 'source', 'keystock').distinct().order_by('-time')
    title_ = []
    time_ = []
    content_ = []
    source_ = []
    keystock_ = []
    index_list = []
    stock_list = ['000001', '399001', '395004', '399005']
    index_dict = latest_index_data(stock_list)
    for key in stock_list:
        index_list.append(index_dict[key]['open'])
    for key in results:
        if key['title'] == title:
            title_ = key['title']
            time_ = key['time']
            content_ = key['content']
            source_ = key['source']
            keystock_ = key['keystock']
            break
    context = {
        'title': title_, 'time': time_, 'content': content_, 'source': source_, 'keystock': res[keystock_[1:7]], 'szzs': index_list[0], 'shenz': index_list[1], 'cyb': index_list[2], 'zxb': index_list[3]
    }
    print(keystock_)
    return HttpResponse(template.render(context, request))
