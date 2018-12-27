from django.urls import path


from . import views


app_name = 'consultant'
urlpatterns = [
	path('', views.index, name = 'consultant'),
	path('<int:share_id>/detail', views.detail_share, name = 'detail_share'),

]