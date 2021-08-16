from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    city = models.CharField(max_length=50, unique=False)
    state = models.CharField(max_length=50, unique=False)

    def __str__(self):
        return self.username
