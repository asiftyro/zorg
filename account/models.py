"""account/models.py"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from simple_history.models import HistoricalRecords
from .managers import AccountManager


class Account(AbstractBaseUser, PermissionsMixin):
    """Account model class"""

    username = models.CharField(max_length=32, unique=True)
    full_name = models.CharField(max_length=64, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=16, unique=True, blank=True, null=True)
    designation = models.CharField(max_length=16, unique=True, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    history = HistoricalRecords()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = AccountManager()

    def __str__(self):
        return f"{self.username}"

    class Meta:
        """Meta for Account"""

        permissions = [
            (
                "selfupdate_account",
                "User Can update his own account",
            ),
        ]
