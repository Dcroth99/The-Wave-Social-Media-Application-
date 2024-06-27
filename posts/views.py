from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Like, User
from users.models import Notification, Profile
from django.db.models import Q


@login_required
def feed(request):
    posts = Post.objects.filter(user__followers__follower=request.user).order_by('-created_at')
    posts_with_comments = {post: post.comments.all() for post in posts}
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'feed.html', {'posts_with_comments': posts_with_comments, 'notifications': notifications})

@login_required
def create_post(request):
    #if request is a post 
    if request.method == 'POST':
        #makes it so the content must be filled out
        content = request.POST['content']
        #assigns the image a var image that gets the image file 
        #but makes it unrequired
        image = request.FILES.get('image')
        #creates a record
        post = Post(user=request.user, content=content, image=image)
        #saves the record
        post.save()
        #redirect tot the name 'feed' in the urls
        return redirect('feed')
    #this happens reguardless of the if statement
    #it's best practice to render the html at the bottom
    return render(request, 'create_post.html')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    
    #.likes is a FK in the Likes model, you can filter the likes on a post by user 
    if post.likes.filter(user=user).exists():

        # Unlike the post
        like = Like.objects.get(user=user, post=post)
        like.delete()
    else:
        # Like the post
        Like.objects.create(user=user, post=post)

        #this checks if the user isn't the post user, that way it will send a notification
        #to the user if someone likes their post
        if user != post.user:
            Notification.objects.create(
                user=post.user,
                sender=user,
                notification_type='like',
                text=f"{user.username} liked your post."
            )
    
    # Redirect to the referring page after liking/unliking
    #request.META.get('HTTP_REFERER' sends the user back to the 
    # same part of the page they were on before the page refreshes
    return redirect(request.META.get('HTTP_REFERER', 'feed'))

@login_required
def comment_post(request, post_id):

    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        content = request.POST['content']
        comment = Comment(user=request.user, post=post, content=content)
        comment.save()

    if request.user != post.user:
        Notification.objects.create(
                    user=post.user,
                    sender=request.user,
                    notification_type='comment',
                    text=f"{request.user.username} commented on your post."
                )
    return redirect(request.META.get('HTTP_REFERER', 'feed'))

@login_required
def delete_post(request, post_id):
    #gets object based on id
    post = get_object_or_404(Post, pk=post_id)
    #checks if the post is the user
    if request.user == post.user:
        #deletes the post
        post.delete()

    return redirect('feed')

@login_required
def clear_notifications(request):
    Notification.objects.filter(user=request.user).delete()
    return redirect('feed')

@login_required
def search(request):
    query = request.GET.get('q')
    post_results = []
    profile_results = []
    if query:
        post_results = Post.objects.filter(Q(content__icontains=query) | Q(user__username__icontains=query))
        profile_results = Profile.objects.filter(Q(user__username__icontains=query))
    return render(request, 'search_results.html', {
        'query': query,
        'post_results': post_results,
        'profile_results': profile_results
    })

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})