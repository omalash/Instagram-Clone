from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'homepage'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('<str:username>/', views.profile, name='profile')
]