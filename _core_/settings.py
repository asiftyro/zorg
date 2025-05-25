"""_core_/settings.py"""

from pathlib import Path
from django.contrib import messages
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Salt
SECRET_KEY = config("SECRET_KEY", cast=str)

# Application run mode
DEBUG = config("DEBUG", cast=bool)

# Hosts
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", cast=Csv())

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "whitenoise.runserver_nostatic",  # vendor
    "crispy_forms",  # vendor
    "crispy_bootstrap5",  # vendor
    "django_tables2",  # vendor
    "django_filters",  # vendor
    "widget_tweaks",  # vendor
    "django_celery_results",  # vendor
    "simple_history",  # vendor
    "zorg",  # custom
    "account",  # custom
    "demo",  # custom
]

# Middlewares
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # vendor, must come after SecurityMiddleware
    "simple_history.middleware.HistoryRequestMiddleware",  # vendor, must come after SecurityMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",  # must come before AuthenticationMiddleware
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "zorg.middleware.CurrentUserMiddleware",  # custom, must come after AuthenticationMiddleware
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Root URL config file
ROOT_URLCONF = "_core_.urls"

# Template settings
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "_templates_"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "zorg.context_processors.verbose_info",  # custom
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = "_core_.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 6,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization/Locale
LANGUAGE_CODE = "en-us"
TIME_ZONE = config("TIME_ZONE", cast=str)
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"

# Static files for Production
STATIC_ROOT = BASE_DIR / "_static_dist_"

# Static files for Development
STATICFILES_DIRS = [
    BASE_DIR / "_static_dev_",
]

# Static file storage
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",  # vendor
    },
}

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Captcha
ALTCHA_HMAC_KEY = config("ALTCHA_HMAC_KEY", cast=str)
ALTCHA_EXPIRE = 60  # minutes
ALTCHA_MAX_NUMBER = 100000

# Session
SESSION_COOKIE_SECURE = DEBUG
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 18000  # in seconds

# Authentication
AUTH_USER_MODEL = "account.Account"
LOGIN_URL = "account:login"
LOGIN_REDIRECT_URL = "demo"  # TODO: set it
LOGOUT_REDIRECT_URL = "account:login"

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", cast=str)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
EMAIL_HOST = config("EMAIL_PORT", cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", cast=str)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", cast=str)

# Celery
CELERY_BROKER_URL = config("CELERY_BROKER_URL", cast=str)  # usually redis://127.0.0.1:6379
CELERY_ACCEPT_CONTENT = {"application/json"}
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_EXTENDED = True
DJANGO_CELERY_RESULTS_TASK_ID_MAX_LENGTH = 191  # for mysql

# Log settings
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "_core_.log_format.JSONFormatter",
        },
        "console": {"()": "_core_.log_format.ConsoleColorFormatter"},
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "json",
            "filename": BASE_DIR / "_logs_/app_log.json",  # TODO: Load from env
            "when": "midnight",
            # backupCount=0, encoding=None, delay=False, utc=False, atTime=None, errors=None
        },
    },
    "loggers": {
        "django": {
            "level": "ERROR",  # TODO: Load from env
            "handlers": ["stdout", "file"],
            "propagate": False,
        },
        "": {
            "level": "DEBUG",  # TODO: Load from env
            "handlers": ["stdout", "file"],
            "propagate": False,
        },
    },
}

# Custom alert/messages
MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

# Crispy form
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"  # vendor
CRISPY_TEMPLATE_PACK = "bootstrap5"  # vendor

# Table style
DJANGO_TABLES2_TABLE_ATTRS = {
    "class": "table table-hover table-condensed table-striped table-hover table-bordered",
    "thead": {
        "class": "table-dark",
    },
}

# Verbose textual info
__VERBOSE_INFO__ = {}
__VERBOSE_INFO__["APP_SHORT_NAME"] = "Zorg"
__VERBOSE_INFO__["APP_COMPANY_SHORT_NAME"] = "Uraal"
__VERBOSE_INFO__["COPYRIGHT_SHORT_TEXT"] = (
    f"{__VERBOSE_INFO__['APP_SHORT_NAME']} © {__VERBOSE_INFO__['APP_COMPANY_SHORT_NAME']}"
)
__VERBOSE_INFO__["SUPPORT_EMAIL"] = "support@example.com"
__VERBOSE_INFO__["SUPPORT_PHONE"] = "+8800123456789"
__VERBOSE_INFO__["SUPPORT_WHATSAPP"] = "8800123456789"  # Don't use + at the beginning
__VERBOSE_INFO__["SUPPORT_TICKET"] = "https://ticket.example.com"

__VERBOSE_INFO__["APP_AUTHOR"] = "Asif R. Porosh"
__VERBOSE_INFO__["APP_DESCRIPTION"] = "Zorg is a django helper app"
__VERBOSE_INFO__["APP_KEYWORDS"] = "Xorg, django, helper"
