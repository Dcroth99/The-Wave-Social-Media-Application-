from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile, Follow, Notification

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    """
        _set is used to after the, 

        lowercase model you wish to get the data from 
        
        gets all the posts made by the user
    
    """ 
    posts = user.post_set.all()
    #Get all users who are following the specified user.
    followers = User.objects.filter(following__following=user)
    #Get all users that the specified user is following.
    following = User.objects.filter(followers__follower=user)
    #checks if the user is following that profile
    is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    #gets the notifications
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'profile.html', {
        'profile': profile,
        'posts': posts,
        'followers': followers,
        'following': following,
        'is_following': is_following,
        'notifications': notifications
    })

@login_required
def follow_unfollow(request, username):
    target_user = get_object_or_404(User, username=username)
    follow, created = Follow.objects.get_or_create(follower=request.user, following=target_user)
    if not created:
        follow.delete()
        Notification.objects.create(
            user=target_user,
            sender=request.user,
            notification_type='unfollow',
            text=f"{request.user.username} has unfollowed you."
        )
    else:
        Notification.objects.create(
            user=target_user,
            sender=request.user,
            notification_type='follow',
            text=f"{request.user.username} has followed you."
        )
    return redirect('profile', username=username)

def home(request):
    if request.user.is_authenticated:
        return redirect('feed')
    return render(request, 'registration/login.html')

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
