from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Follow

@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    posts = user.post_set.all()
    followers = user.followers.all()
    following = user.following.all()
    is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    return render(request, 'profile.html', {'profile': profile, 'posts': posts, 'followers': followers, 'following': following, 'is_following': is_following})

@login_required
def follow_unfollow(request, username):
    target_user = User.objects.get(username=username)
    follow, created = Follow.objects.get_or_create(follower=request.user, following=target_user)
    if not created:
        follow.delete()
    return redirect('profile.html', username=username)


