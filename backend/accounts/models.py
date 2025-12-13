# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(
        blank=True,
        null=True
    )

    REQUIRED_FIELDS = []  # superuser email 강제 제거
