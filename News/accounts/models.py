from django.contrib.auth import base_user as auth_user
from django.contrib.auth import models as auth_models
from django.db import models
from .managers import NewsUserManager
# Create your models here.



class NewsUser(auth_user.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        unique=True,
        max_length=255,
    )

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    object = NewsUserManager()

    def __str__(self):
        return self.email
