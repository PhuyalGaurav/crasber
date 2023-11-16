from django.contrib.auth.models import AbstractUser
from django.db import models
import random
import os

class User(AbstractUser):
    def path_for_user(self, request):
        if not os.path.exists(f'media/pfp/{self.username}'):
            os.mkdir(f'media/pfp/{self.username}')
        return f'media/pfp/{self.username}'
    
    default_pfp_location = f"pfp/defaults/{random.randrange(1,10)}.png"
    follower = models.TextField(default="", null=True)
    following = models.TextField(default="", null=True)
    bio = models.TextField(default="", null=True)
    pfp = models.ImageField(upload_to=path_for_user,blank=True, null=True)
    def_pfp = models.ImageField(default=default_pfp_location)

    def get_pfp(self):
        if self.pfp:
            return self.pfp
        else:
            return self.def_pfp

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    edited = models.BooleanField(default=False)
    likers = models.TextField(default="", null=True)

    def __str__(self):
        return f'{self.user} has posted {self.content} at {self.creation_date}'

