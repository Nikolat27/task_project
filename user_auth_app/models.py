from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True) # Username and email must be unique
    email = models.EmailField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False) #
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.username}"
