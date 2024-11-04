from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Moderator', 'Moderator'),
        ('Superadmin', 'Superadmin'),
        ('User', 'User'),  
    ]
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='User')
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return self.username
