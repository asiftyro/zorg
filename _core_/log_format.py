import logging
import json_log_formatter
from django.utils import timezone
from colorama import Fore, Style


class JSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message, extra, record):
        extra.update(
            {
                "time": timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S.%f %z"),
                "level": record.levelname,
                "message": message,
                "name": record.name,
                "filename": record.filename,
                "module": record.module,
                "funcName": record.funcName,
                "lineno": record.lineno,
                "pathname": record.pathname,
                "stack_info": record.stack_info,
            }
        )
        return super().json_record(message, extra, record)


class ConsoleColorFormatter(logging.Formatter):

    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: Fore.LIGHTMAGENTA_EX + format + Style.RESET_ALL,
        logging.INFO: Fore.CYAN + Style.BRIGHT + format + Style.RESET_ALL,
        logging.WARNING: Fore.YELLOW + Style.BRIGHT + format + Style.RESET_ALL,
        logging.ERROR: Fore.RED + Style.BRIGHT + format + Style.RESET_ALL,
        logging.CRITICAL: Fore.RED + Style.BRIGHT + format + Style.RESET_ALL,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
