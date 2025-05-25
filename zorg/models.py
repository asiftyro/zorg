# zorg/models.py
from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords
from zorg.middleware import get_current_user


class AuditModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created",
        editable=False,
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_modified",
        editable=False,
    )

    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()
        if not self.pk and not self.created_by:
            self.created_by = user
        else:
            self.modified_by = user
        super().save(*args, **kwargs)
