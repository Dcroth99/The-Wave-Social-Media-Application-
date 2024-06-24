from django.urls import path
from . import views

urlpatterns = [
    path('feed/', views.feed, name='feed'),
    path('create/', views.create_post, name='create_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.comment_post, name='comment_post'),
    
]