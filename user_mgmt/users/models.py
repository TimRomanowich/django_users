from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

User.add_to_class('last_activity', models.DateTimeField(default=timezone.now))