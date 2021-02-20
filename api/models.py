from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    email = models.EmailField(
        max_length=100,
        unique=True,
        db_index=True,
    )
    last_request = models.DateTimeField(
        default=timezone.now
    )
    
    def __str__(self):
        return self.username


class Post(models.Model):
    title = models.CharField(max_length=100) 
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        to=User, 
        null=True, 
        on_delete=models.SET_NULL, 
        related_name='created_post'
    )
    changed_by = models.ForeignKey(
        to=User, 
        null=True, 
        on_delete=models.SET_NULL, 
        related_name='changed_post'
    )

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title


class Like(models.Model):
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name="likes"
    )
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        to=User, 
        null=True, 
        on_delete=models.SET_NULL, 
        related_name='created_like'
    )
    changed_by = models.ForeignKey(
        to=User, 
        null=True, 
        on_delete=models.SET_NULL, 
        related_name='changed_like'
    )

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

    def __str__(self):
        return f"{self.created_by} liked {self.post}"
