from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(
        max_length=100,
        unique=True,
        db_index=True,
    )
    last_visit = models.DateTimeField(auto_now=True, editable=False)


