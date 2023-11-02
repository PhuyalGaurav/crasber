from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follower = models.TextField(default="", null=True)
    following = models.TextField(default="", null=True)
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user} has posted {self.content} at {self.creation_date}'

