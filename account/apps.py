"""account/apps.py"""

from django.apps import AppConfig


class AccountConfig(AppConfig):
    """account config"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "account"
    label = "account"
    verbose_name = "User Account"
