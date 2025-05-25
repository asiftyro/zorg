"""zorg/management/commands/cookapp.py"""

import re
import uuid
import base64
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from django.apps import apps
from .utils import echo


class Command(BaseCommand):

    def add_arguments(self, parser):
        # parser.add_argument("app-name", nargs=1, type=str)
        parser.add_argument("app-name", action="store", default="", type=str, help="name of the app")
        parser.add_argument("-f", "--force", action="store_true", default=False, help="overwrite app if exist")

    def shape_mold(
        self,
        content,
        app_name,
        app_label,
        app_dir_name,
        model_name,
        verbose_name,
        menu_id,
        permission_suffix,
    ):
        shaped = content
        shaped = shaped.replace("___APP_NAME___", app_name)
        shaped = shaped.replace("___APP_LABEL___", app_name)
        shaped = shaped.replace("___MODEL_NAME___", model_name)
        shaped = shaped.replace("___APP_DIR_NAME___", app_dir_name)
        shaped = shaped.replace("___VERBOSE_NAME___", verbose_name)
        shaped = shaped.replace("___MENU_ID___", menu_id)
        shaped = shaped.replace("___PERMISSION_SUFFIX___", permission_suffix)
        return shaped

    def handle(self, *args, **options):
        # echo = self.stdout.write
        # success = self.style.SUCCESS
        # warn = self.style.WARNING
        # error = self.style.ERROR
        # notice = self.style.NOTICE

        app_name = options["app-name"]

        if not bool(re.fullmatch(r"[a-z].*[a-z0-9]+(_[a-z0-9]+)*", app_name)):
            echo(self, "e", "Invalid input. app-name must be in snake-case")
            return

        APP_DIR_NAME = app_name.lower().replace("_", "").replace("-", "")
        APP_NAME = APP_DIR_NAME
        APP_LABEL = APP_DIR_NAME

        _name_parts = []
        for _model_name in app_name.split("-"):
            _name_parts += _model_name.split("_")

        VERBOSE_NAME = " ".join(_model_name.capitalize() for _model_name in _name_parts)
        MODEL_NAME = "".join(_model_name.capitalize() for _model_name in _name_parts)
        PERMISSION_SUFFIX = f"_{MODEL_NAME.lower()}"
        PERMISSION_PREFIX = ["add", "change", "delete", "view"]
        APP_DIR_PATH = settings.BASE_DIR / APP_DIR_NAME

        uuid_bytes = uuid.uuid4().bytes
        short_uuid = base64.urlsafe_b64encode(uuid_bytes).rstrip(b"=").decode("utf-8")

        MENU_ID = f"{APP_NAME}-{short_uuid}"

        if not options["force"] and APP_NAME in [app.name for app in apps.get_app_configs()]:
            echo(self, "e", f"App: <{app_name}> exists!")
            return
        FILE_NAME_DICT = {
            "MODELS_PY": Path(APP_DIR_PATH / "models.py"),
            "VIEWS_PY": Path(APP_DIR_PATH / "views.py"),
            "TABLES_PY": Path(APP_DIR_PATH / "tables.py"),
            "FILTERS_PY": Path(APP_DIR_PATH / "filters.py"),
            "URLS_PY": Path(APP_DIR_PATH / "urls.py"),
            "FORMS_PY": Path(APP_DIR_PATH / "forms.py"),
            "TESTS_PY": Path(APP_DIR_PATH / "tests.py"),
            "APPS_PY": Path(APP_DIR_PATH / "apps.py"),
            "ADMIN_PY": Path(APP_DIR_PATH / "admin.py"),
            "APP_INIT_PY": Path(APP_DIR_PATH / "__init__.py"),
            "MIGRATION_INIT_PY": Path(APP_DIR_PATH / "migrations" / "__init__.py"),
            "TEMPLATE_FORM_HTML": Path(APP_DIR_PATH / "templates" / APP_NAME / f"{APP_NAME}_form.html"),
            "TEMPLATE_FILTER_HTML": Path(APP_DIR_PATH / "templates" / APP_NAME / f"{APP_NAME}_filter.html"),
            "TEMPLATE_DETAIL_HTML": Path(APP_DIR_PATH / "templates" / APP_NAME / f"{APP_NAME}_detail.html"),
            "TEMPLATE_CONFIRM_DELETE_HTML": Path(
                APP_DIR_PATH / "templates" / APP_NAME / f"{APP_NAME}_confirm_delete.html"
            ),
            "TEMPLATE_SIDE_NAV_URLS_HTML": Path(
                APP_DIR_PATH / "templates" / APP_NAME / f"{APP_NAME}_side_nav_urls.html"
            ),
        }

        echo(self, "s", f"Cooking: {APP_NAME}")
        echo(self, None)
        echo(self, "w", f"APP_NAME: {APP_NAME}")
        echo(self, "w", f"APP_LABEL: {APP_LABEL}")
        echo(self, "w", f"APP_DIR_PATH: {APP_DIR_PATH}")
        echo(self, "w", f"VERBOSE_NAME: {VERBOSE_NAME}")
        echo(self, "w", f"MODEL_NAME: {MODEL_NAME}")

        echo(self, "w", "PERMISSIONS:")
        for prx in PERMISSION_PREFIX:
            echo(self, "w", f"  {APP_LABEL}.{prx}{PERMISSION_SUFFIX}")

        for f_key in FILE_NAME_DICT:
            f_path = FILE_NAME_DICT[f_key]
            mold_file = open(Path(__file__).parent.resolve() / "molds" / f"{f_key}.txt", "r")
            content = mold_file.read()
            shaped_content = self.shape_mold(
                content,
                APP_NAME,
                APP_LABEL,
                APP_DIR_NAME,
                MODEL_NAME,
                VERBOSE_NAME,
                MENU_ID,
                PERMISSION_SUFFIX,
            )
            mold_file.close()

            f_path.parent.mkdir(parents=True, exist_ok=True)
            f_path.write_text(shaped_content)

        echo(self, None, "")
        echo(self, None, f"* Add '{APP_NAME}' in  _core_.settings.INSTALLED_APPS")
        echo(self, None, f"* Include '{APP_NAME}.urls' in  _core_.urls.urlpatterns")
        echo(self, None, "")
        echo(self, "s", f"Coooked: {APP_NAME}. Bye!")
        return
