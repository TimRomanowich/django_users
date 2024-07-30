from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

User.add_to_class('last_activity', models.DateTimeField(default=timezone.now))

class ChatPrivilege(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    can_post = models.BooleanField(default=True)
    can_read = models.BooleanField(default=True)
    can_post_media = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s chat privileges"
    
    def update_privileges(self, can_post=None, can_read=None, can_post_media=None):
        if can_post is not None:
            self.can_post = can_post
        if can_read is not None:
            self.can_read = can_read
        if can_post_media is not None:
            self.can_post_media = can_post_media
        self.save()
        