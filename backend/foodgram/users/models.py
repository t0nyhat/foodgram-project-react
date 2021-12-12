from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    CHOICES = [
        (USER, 'user'),
        (ADMIN, 'admin'),
    ]
    first_name = models.CharField(
        'first_name',
        max_length=150, )

    last_name = models.CharField(
        'last_name',
        max_length=150, )

    username = models.CharField(
        'username',
        unique=True,
        max_length=150)

    email = models.EmailField(
        'email',
        unique=True,
        max_length=254
    )

    role = models.CharField(
        'role',
        max_length=len(max((role_pair[1] for role_pair in CHOICES), key=len)),
        choices=CHOICES,
        default=USER
    )

    def __str__(self):
        return self.username

    REQUIRED_FIELDS = ['email', 'last_name', 'first_name']

    @property
    def is_admin(self):
        return (
            self.is_superuser
            or self.is_staff
            or self.role == User.ADMIN)

    class Meta:
        ordering = ['username']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
