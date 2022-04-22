from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    email = models.CharField(max_length=255)

    # For logging in
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    username = None
    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []
