from django.urls import path

from . import views
# Create your urls here.

app_name = 'stock_choice'
urlpatterns = [
	path('', views.index, name = 'stock_choice'),
	path('<int:stock_id>/detail', views.detail_stock, name = 'detail_stock'),
]