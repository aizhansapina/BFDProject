from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100)
    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.CharField(max_length = 200)
    author = models.ForeignKey(User , on_delete = models.CASCADE)
    post = models.ForeignKey(Post , on_delete = models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.text


class Repost(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username + ' reposted '+self.post.title



