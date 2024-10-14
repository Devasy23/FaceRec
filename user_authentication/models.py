from django.contrib.auth.models import AbstractUser
from django.db import models

# Choices for roles
ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('user', 'User'),
)

# Custom user model with roles
class CustomUser(AbstractUser):
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username
