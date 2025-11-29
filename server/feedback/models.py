from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

# Create your models here.


class Feedback(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.TextField()
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
