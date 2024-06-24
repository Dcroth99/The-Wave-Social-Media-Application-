from django.shortcuts import render, redirect
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
    post = Post.objects.get(id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('feed')

@login_required
def comment_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        content = request.POST['content']
        comment = Comment(user=request.user, post=post, content=content)
        comment.save()
    return redirect('feed')

