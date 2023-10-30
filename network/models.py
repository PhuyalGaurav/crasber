from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class NewPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} has posted {self.post_content} at {self.creation_date}'

