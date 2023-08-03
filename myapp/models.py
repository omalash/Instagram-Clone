from django.contrib.auth.models import User
from django.db import models
import os

def profile_picture_path(instance, filename):
    # Upload path for user profile pictures
    return os.path.join('profile_pictures', f'user_{instance.user.id}/{instance.user.username}', filename)

def post_image_path(instance, filename):
    # Upload path for post images
    return os.path.join('post_images', f'user_{instance.profile.user.id}/{instance.profile.user.username}', filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    description = models.CharField(max_length=150, default="", null=True)
    pfp = models.ImageField(upload_to=profile_picture_path, default="default_pfp.jpg", null=True)
    following = models.ManyToManyField(User, related_name='following', symmetrical=False)
    followers = models.ManyToManyField(User, related_name='followers', symmetrical=False)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    caption = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to=post_image_path)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Profile, related_name='post_likes')

class Comment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Profile, related_name='comment_likes')

    def __str__(self):
        return self.caption