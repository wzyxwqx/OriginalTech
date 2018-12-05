from django.shortcuts import render
from django.template import loader


# code here

def index(request):
	return render(request, 'ecoinfor/pagejump.html')