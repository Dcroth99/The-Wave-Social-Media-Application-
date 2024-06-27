from django.urls import path
from . import views

urlpatterns = [
    path('feed/', views.feed, name='feed'),
    path('create/', views.create_post, name='create_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.comment_post, name='comment_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('clear-notifications/', views.clear_notifications, name='clear_notifications'),
    path('search/', views.search, name='search'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]
