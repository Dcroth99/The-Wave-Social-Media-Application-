from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:username>/', views.profile, name='profile'),
    path('follow/<str:username>/', views.follow_unfollow, name='follow_unfollow'),
    
]