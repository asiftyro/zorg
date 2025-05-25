"""zorg/management/commands/cookapp.py"""

import re
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings

from .utils import echo, COMMAND_DIR_ROOT, copy_files
import sass

CSS_HEADER_COMMENT = """/*
Zorg, compiled by - Asif R. Porosh. Mailto: asif.tyro@gmail.com
Based on -
    bootswatch 5.3.3
    bootstrap 5.3.3
    bootstrap icon 1.11.3
*/
"""


class Command(BaseCommand):

    def handle(self, *args, **options):
        echo(self, "s", "Cooking styles!")

        dest_dir_css = settings.STATICFILES_DIRS[0] / "css"
        dest_dir_js = settings.STATICFILES_DIRS[0] / "js"
        dest_dir_img = settings.STATICFILES_DIRS[0] / "img"
        dest_dir_font = settings.STATICFILES_DIRS[0] / "font"
        template_dir = settings.TEMPLATES[0]["DIRS"][0]

        Path(dest_dir_css).mkdir(parents=True, exist_ok=True)
        Path(dest_dir_js).mkdir(parents=True, exist_ok=True)
        Path(dest_dir_img).mkdir(parents=True, exist_ok=True)
        Path(dest_dir_font).mkdir(parents=True, exist_ok=True)

        copy_files(COMMAND_DIR_ROOT / "font", dest_dir_font)
        copy_files(COMMAND_DIR_ROOT / "js", dest_dir_js)
        copy_files(COMMAND_DIR_ROOT / "img", dest_dir_img)

        url_accumulator = COMMAND_DIR_ROOT.parent.parent / "templates/zorg/side_nav_urls.html"
        if not url_accumulator.exists():
            copy_files(url_accumulator, template_dir)

        dest_css_file_path = settings.STATICFILES_DIRS[0] / "css/styles.css"
        source = str(COMMAND_DIR_ROOT / "scss/styles.scss")
        css_output = sass.compile(filename=source, output_style="compressed")
        css_cleaned = re.sub("/\\*[^*]*\\*+(?:[^/*][^*]*\\*+)*/", "", css_output)
        css_cleaned = css_cleaned.replace("\ufeff", "")
        css_with_heder_comment = CSS_HEADER_COMMENT + css_cleaned.strip()
        with open(dest_css_file_path, "w") as css_file:
            css_file.write(css_with_heder_comment)
        echo(self, "s", "Styles cooked!")
        return
