from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    profile_picture_url = models.URLField(blank=True, null=True)

class Chat(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    assistant_id = models.CharField(max_length=255)
    thread_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    messages = models.JSONField(default=list)

    def __str__(self):
        return f'{self.user.username} - Last updated: {self.updated_at}'
