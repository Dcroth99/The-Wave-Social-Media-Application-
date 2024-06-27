from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    #creates a user from the imported User model 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #makes the content a text field
    content = models.TextField()
    """ uploads all post images to a directory called 'post_images/',
        blank = True to allow it to be left blank,
        and null = True to allow the database
        to store it as a null value incase its left blank """
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def __str__(self):
        return self.content[:50]
        #displays only the first 50 characters in the admin site 

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]
        #displays only the first 50 characters in the admin site 
    
    def children(self):
        return self.replies.all()
    
    @property
    def is_parent(self):
        return self.parent is None



class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f'{self.user.username} likes {self.post.content[:20]}'
        #displays only the first 20 characters in the admin site 