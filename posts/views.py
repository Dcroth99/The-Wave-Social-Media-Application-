from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Like

@login_required
def feed(request):
    posts = Post.objects.filter(user__followers__follower=request.user).order_by('-created_at')
    return render(request, 'feed.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST['content']
        image = request.FILES.get('image')
        post = Post(user=request.user, content=content, image=image)
        post.save()
        return redirect('feed')
    return render(request, 'create_post.html')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    
    if post.likes.filter(user=user).exists():
        # Unlike the post
        like = Like.objects.get(user=user, post=post)
        like.delete()
    else:
        # Like the post
        Like.objects.create(user=user, post=post)
    
    # Redirect to the referring page after liking/unliking
    return redirect(request.META.get('HTTP_REFERER', 'feed'))

@login_required
def comment_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        content = request.POST['content']
        comment = Comment(user=request.user, post=post, content=content)
        comment.save()
    return redirect('feed')

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user == post.user:
        post.delete()
    return redirect('feed')