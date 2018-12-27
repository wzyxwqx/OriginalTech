from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'users'
urlpatterns = [
#        url(r'^register/', views.RegisterView.as_view(), name='register')
        path('register/', views.RegisterView.as_view(), name='register'),
        path('registration_success/', views.SuccessView.as_view(), name='success')
]
