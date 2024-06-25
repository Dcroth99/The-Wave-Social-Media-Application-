from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile, Follow

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    posts = user.post_set.all()
    followers = User.objects.filter(following__following=user)
    following = User.objects.filter(followers__follower=user)
    is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    
    return render(request, 'profile.html', {
        'profile': profile,
        'posts': posts,
        'followers': followers,
        'following': following,
        'is_following': is_following
    })

@login_required
def follow_unfollow(request, username):
    target_user = get_object_or_404(User, username=username)
    follow, created = Follow.objects.get_or_create(follower=request.user, following=target_user)
    if not created:
        follow.delete()
    return redirect('profile', username=username)

def home(request):
    if request.user.is_authenticated:
        return redirect('feed')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)  # Create a profile for the new user
            login(request, user)
            return redirect('feed')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('feed')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')