import logging

from config import config


class Colors:
    """ANSI color codes"""

    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"

    # cancel SGR codes if we don't write to a terminal
    if not __import__("sys").stdout.isatty():
        for _ in dir():
            if _[0] != "_":
                locals()[_] = ""
    else:
        # set Windows console in VT mode
        if __import__("platform").system() == "Windows":
            kernel32 = __import__("ctypes").windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            del kernel32


class LoggerFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG: Colors.DARK_GRAY + "%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s" + Colors.END,
        logging.INFO: Colors.GREEN + "%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s" + Colors.END,
        logging.WARNING: Colors.YELLOW + "%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s" + Colors.END,
        logging.ERROR: Colors.RED + "%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s" + Colors.END,
        logging.CRITICAL: Colors.LIGHT_RED + "%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s" + Colors.END,
    }

    def format(self, record: logging.LogRecord):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


# define custom log level names
log_levels = {"debug": logging.DEBUG, "info": logging.INFO,
              "warn": logging.WARNING, "error": logging.ERROR}


logging.addLevelName(logging.DEBUG, "debug")
logging.addLevelName(logging.INFO, "info ")
logging.addLevelName(logging.WARNING, "warn ")
logging.addLevelName(logging.ERROR, "error")

log_level = log_levels.get(config.LOG_LEVEL, logging.DEBUG)

global_formatter = LoggerFormatter()
global_handler = logging.StreamHandler()
global_handler.setLevel(log_level)
global_handler.setFormatter(global_formatter)


def logger_factory(name: str):
    name_logger = logging.getLogger(name)

    for handler in name_logger.handlers:
        name_logger.removeHandler(handler)

    name_logger.setLevel(log_level)
    name_logger.addHandler(global_handler)

    return name_logger


def init_module_loggers(*args: str):
    for logger_name in args:
        module_logger = logging.getLogger(logger_name)

        for handler in module_logger.handlers:
            module_logger.removeHandler(handler)

        module_logger.setLevel(log_level)
        module_logger.addHandler(global_handler)


def update_formatters(*args: str):
    for logger_name in args:
        module_logger = logging.getLogger(logger_name)

        for handler in module_logger.handlers:
            module_logger.removeHandler(handler)

        module_logger.addHandler(global_handler)


logger = logging.getLogger(__name__)
logger.setLevel(log_level)
logger.addHandler(global_handler)

loggers = [logging.getLogger().name] + [
    lg for lg in logging.Logger.manager.loggerDict.keys()
]


logger.debug(loggers)


def init_logging():
    update_formatters(*loggers)
    # init_module_loggers('root', 'agno', 'fastapi', 'uvicorn', 'pylance')


__all__ = ["init_module_loggers", "update_formatters", "logger"]





