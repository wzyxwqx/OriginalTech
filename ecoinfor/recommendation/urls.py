from django.urls import path

from . import views

app_name = 'recommendation'
urlpatterns = [
	path('', views.index, name = 'recommendation'),
	path('<int:news_id>/detail', views.detail_news, name = 'detail_news'),
]