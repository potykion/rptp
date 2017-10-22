from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    AbstractUser with VK access token and user id.
    """
    access_token = models.CharField(max_length=200)
    user_id = models.IntegerField(null=True)
