"""zorg/management/commands/seeddb.py"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps


class Command(BaseCommand):

    def handle(self, *args, **options):
        echo = self.stdout.write
        success = self.style.SUCCESS
        warn = self.style.WARNING
        error = self.style.ERROR
        notice = self.style.NOTICE

        all_models = apps.get_models()
        echo(success("Ello"))
        for index, model in enumerate(all_models):
            echo(warn(f"# {index + 1}."))
            echo(warn(f"Model: {model.__name__}"))
            echo(notice(f"File path: {model.__module__.replace('.', '/')}.py"))
            echo(notice("-" * 60))
        echo(success("Bi"))
