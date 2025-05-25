"""zorg/context_processors.py"""

from django.conf import settings
from django.utils import timezone


def verbose_info(request):
    return settings.__VERBOSE_INFO__
