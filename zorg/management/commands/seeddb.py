"""zorg/management/commands/seeddb.py"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


_SUPER_USER_ = "superadmin"


_PASSWORD_ = "password1"

_GROUPS_ = {
    "MAKER": {
        "apps": {
            # "app_label": "matching string in permission to exclude",
            "vehicles": "",
            "office": "",
            "vehicle_supplier": "",
            "maintenance_vendor": "",
            "drivers": "",
            "vehicle_type": "",
            "maintenance_requisition": "checker",
            "vehicle_requisition": "checker",
        },
        "users": [
            "maker1",
            "maker2",
            "maker3",
        ],
    },
    "CHECKER": {
        "apps": {
            # "app_label": "matching string in permission to exclude",
            "maintenance_requisition": "maker",
            "vehicle_requisition": "maker",
        },
        "users": [
            "checker1",
            "checker2",
            "checker3",
        ],
    },
    "SUPERVISOR": {
        "apps": {
            # "app_label": "matching string in permission to exclude",
            "vehicles": "",
            "office": "",
            "vehicle_supplier": "",
            "maintenance_vendor": "",
            "drivers": "",
            "vehicle_type": "",
            "maintenance_requisition": "",
            "vehicle_requisition": "",
        },
        "users": [
            "supervisor1",
            "supervisor2",
            "supervisor3",
        ],
    },
    "ADMIN": {
        "apps": {
            # "app_label": "matching string in permission to exclude",
            "account": "",
        },
        "users": [
            "admin1",
            "admin2",
            "admin3",
        ],
    },
}


def init_user(user, echo, success, warn, error):
    """init user"""
    user_model = get_user_model()
    try:
        new_user = user_model.objects.get(username=user)
        echo(warn(f"User: '{user}' already exists."))
    except user_model.DoesNotExist:
        new_user = user_model.objects.create_superuser(username=user, password=_PASSWORD_)
        echo(success(f"User: '{user}' created."))
    return new_user


def init_superuser(echo, success, warn, error):
    """init user"""
    user_model = get_user_model()
    new_user = user_model.objects.filter(username=_SUPER_USER_)
    if new_user.exists():
        echo(warn(f"Speruser: '{_SUPER_USER_}' already exists."))
    else:
        new_user = user_model.objects.create_superuser(username=_SUPER_USER_, password=_PASSWORD_)
        echo(success(f"Speruser: '{_SUPER_USER_}' created."))
    return new_user


def init_group(group, echo, success, warn, error):
    """init group"""
    group, created = Group.objects.get_or_create(name=group)
    if created:
        echo(success(f"Group: '{group.name}' created."))
    else:
        echo(warn(f"Group: '{group.name}' already exists."))
    return group


def init(group_dict, echo, success, warn, error):
    """init group permissions add add users to groups"""
    init_superuser(echo, success, warn, error)
    for grp in group_dict:
        group_obj = init_group(grp, echo, success, warn, error)
        for app in group_dict[grp]["apps"]:
            content_types = ContentType.objects.filter(app_label=app)
            permissions = Permission.objects.filter(content_type__in=content_types)

            for perm in permissions:
                exculsion_string = group_dict[grp]["apps"][app]
                if exculsion_string and exculsion_string in perm.codename:
                    echo(warn(f"Permission: '{perm.codename}' not added to group: '{group_obj.name}'."))
                else:
                    group_obj.permissions.add(perm)
                    echo(success(f"Permission: '{perm.codename}' added to group: '{group_obj.name}'."))
                for user in group_dict[grp]["users"]:
                    new_user = init_user(user, echo, success, warn, error)
                    new_user.groups.add(group_obj)
                    echo(success(f"User: '{new_user}' added to group: '{group_obj.name}'."))


class Command(BaseCommand):

    def handle(self, *args, **options):
        echo = self.stdout.write
        success = self.style.SUCCESS
        warn = self.style.WARNING
        error = self.style.ERROR
        echo(success("Hello Wald!"))
        init(_GROUPS_, echo, success, warn, error)
        echo(success("Tha Tha Wald!"))
        return
