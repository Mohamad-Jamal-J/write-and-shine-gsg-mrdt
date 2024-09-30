from django.db import models
from django.contrib.auth import get_user_model
import os

User = get_user_model()


class Profile(models.Model):
    """
    Profile model for extending the User model with additional information.
    Each user has one profile with optional fields for headline, bio, profile picture, and education.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    headline = models.CharField(max_length=70, blank=True, default="")
    bio = models.TextField(blank=True, default="")
    profile_picture = models.ImageField(upload_to='media/profile_pictures/', blank=True, null=True)
    education = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return f"{self.user.name}'s Profile"

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = Profile.objects.get(pk=self.pk)
            if old_instance.profile_picture and old_instance.profile_picture != self.profile_picture:
                if os.path.isfile(old_instance.profile_picture.path):
                    os.remove(old_instance.profile_picture.path)

        super().save(*args, **kwargs)
