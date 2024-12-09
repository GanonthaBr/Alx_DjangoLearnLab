from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

#custon user
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True)
    # profile_pic = models.ImageField(upload_to='profile_pics/',blank=True, null=True)
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title