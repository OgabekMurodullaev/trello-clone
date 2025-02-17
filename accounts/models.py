from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import UserManager


class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatars/")
    bio = models.CharField(max_length=120)
    username = models.CharField(max_length=150,
                                error_messages={"unique": "A user with that username already exists"},
                                null=True,
                                blank=True)
    is_active = models.BooleanField(default=False, help_text=("Designates whether this user should be treated as active. "
                                                              "Unselect this instead of deleting accounts."))
    USERNAME_FIELD = "email"
    objects = UserManager()
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email