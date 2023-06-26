from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='homepage'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('create_post', views.create_post, name='create_post'),
    path('<str:username>/edit_profile', views.edit_profile, name='edit_profile'),
    path('search/', views.search, name='search'),
    path('<str:username>/', views.profile, name='profile'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)