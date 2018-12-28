from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('login/success/', views.SuccessView.as_view(), name='login_success'),
    path('logout/success/', views.SuccessView.as_view(), name='logout_success'),
    path('select_new_stocks/', views.select_new_stocks, name='select_new_stocks'),
    path('search_new_stocks/', views.search_new_stocks, name='search_new_stocks'),
    path('users_stocks/', views.users_stocks, name='users_stocks'),
    path('re_login', views.re_login.as_view(), name = 're_login'),

    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(), name='login'),
]
