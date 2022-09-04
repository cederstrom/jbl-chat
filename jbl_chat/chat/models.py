from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Message(models.Model):
    content = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
