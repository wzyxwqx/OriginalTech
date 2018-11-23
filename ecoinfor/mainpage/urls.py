from django.urls import path


from . import views


app_name = 'mainpage'
urlpatterns = [
	path('', views.index, name = 'mainpage'),
	path('<int:message_id>/detail', views.detail_message, name = 'detail_message'),
#	path('<int:pk>/message', view.message, name = 'message')
]