from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

@receiver(post_save, sender="auth.User")  # new
def create_or_update_user_profile(sender, instance, created, **kwargs):
    Profile.objects.get_or_create(user=instance)
