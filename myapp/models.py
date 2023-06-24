from django.contrib.auth.models import User
from django.db import models
import os

def user_profile_picture_path(instance, filename):
    # Upload path for user profile pictures
    return os.path.join('profile_pictures', f'user_{instance.user.username}', filename)

def post_image_path(instance, filename):
    # Upload path for post images
    return os.path.join('post_images', f'user_{instance.user_profile.user.username}', filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    description = models.CharField(max_length=150, default="", null=True)
    pfp = models.ImageField(upload_to=user_profile_picture_path, default="default_pfp.jpg", null=True)
    following = models.ManyToManyField(User, related_name='followers')
    followers = models.ManyToManyField(User, related_name='following')

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posts')
    caption = models.CharField(max_length=500, null=True)
    image = models.ImageField(upload_to=post_image_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption