"""
WSGI config for _core_ project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.conf import settings
from colorama import Fore, Back, Style

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_core_.settings")

print(
    "\n"
    + Fore.WHITE
    + Back.YELLOW
    + " Settings loaded. Debug mode : "
    + Back.RED
    + Fore.WHITE
    + f" {settings.DEBUG} "
    + Style.RESET_ALL
    + "\n"
)

application = get_wsgi_application()
