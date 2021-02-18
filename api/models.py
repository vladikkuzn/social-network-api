from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(
        max_length=100,
        unique=True,
        db_index=True,
    )
    last_visit = models.DateTimeField(auto_now=True, editable=False)


class Post(models.Model):
    title = models.CharField(max_length=100) 
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='created_post')
    changed_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='changed_post')


    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

