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
    path('like_post/<int:post_id>/', views.add_like_to_post, name='add_like_to_post'),
    path('follow_user/<str:username>/', views.follow_user, name='follow_user')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)