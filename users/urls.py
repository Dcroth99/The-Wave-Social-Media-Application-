from django.urls import path
from .views import profile, follow_unfollow, home, register, login_view, logout_view

urlpatterns = [
    path('home/', home, name='home'),
    path('profile/<str:username>/', profile, name='profile'),
    path('follow/<str:username>/', follow_unfollow, name='follow_unfollow'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]