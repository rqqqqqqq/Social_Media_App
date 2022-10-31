from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

from .views import home_screen_post



urlpatterns=[
    # path('', views.home_screen_view, name='home'),
    path('', home_screen_post.as_view(), name='home'),


    path('register/', views.register_view, name="register"), 
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    # path('login/', views.login_view, name="login"), 
    # path('logout/', views.logout_view, name="logout"),
    
    path('account/<user_id>/', views.account_view, name='profile'), 
    path('search/', views.search_user, name="search"), 
    path('friend/friend_request/', views.send_friend_request, name='friend-request'),
    path('chat/', views.index, name='index'),
    path('chat/<str:room_name>/', views.room, name='room'),




    # path('', views.index, name='index'),
    # path('<str:room_name>/', views.room, name='room'),

    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




