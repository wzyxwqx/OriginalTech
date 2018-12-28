from django.urls import path, include


from . import views


app_name = 'mainpage'
urlpatterns = [
	path('', views.index, name = 'mainpage'),
	# path('', views.index, name = 'mainpage'),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path(('<str:title>/'), views.content_index, name = 'content'),
#	path('<int:pk>/News', view.News, name = 'News')
]