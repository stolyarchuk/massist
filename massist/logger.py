import logging
from typing import Any

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
        logging.DEBUG: Colors.DARK_GRAY + "[%(levelname)s] [%(name)s] %(message)s" + Colors.END,
        logging.INFO: Colors.GREEN + "[%(levelname)s] [%(name)s] %(message)s" + Colors.END,
        logging.WARNING: Colors.YELLOW + "[%(levelname)s] [%(name)s] %(message)s" + Colors.END,
        logging.ERROR: Colors.RED + "[%(levelname)s] [%(name)s] %(message)s" + Colors.END,
        logging.CRITICAL: Colors.LIGHT_RED + "[%(levelname)s] [%(name)s] %(message)s" + Colors.END,
    }

    def format(self, record: logging.LogRecord):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


# define custom log level names
logging.addLevelName(logging.DEBUG, "debug")
logging.addLevelName(logging.INFO, "info ")
logging.addLevelName(logging.WARNING, "warn ")
logging.addLevelName(logging.ERROR, "error")

log_levels = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warn": logging.WARNING,
    "error": logging.ERROR,
}

log_level = log_levels.get(config.LOG_LEVEL, logging.DEBUG)


class Logger:
    """
    Singleton Logger class that encapsulates all logging functionality.
    """

    _instance = None
    _logger: logging.Logger

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the logger instance"""
        self._logger = self.get_logger(__name__)

    def get_logger(self, name: str | None = None) -> logging.Logger:
        """
        Creates and configures a logger with the specified name.

        Args:
            name (str): The name for the logger. Defaults to module name.

        Returns:
            logging.Logger: A configured logger instance
        """

        if name is None:
            name = __name__

        new_logger = logging.getLogger(name)
        new_logger.propagate = False
        new_logger.setLevel(log_level)

        # Remove any existing handlers to avoid duplicate logs
        for handler in new_logger.handlers:
            new_logger.removeHandler(handler)

        new_logger.addHandler(self._get_handler())
        new_logger.debug("Created logger: %s", name)

        return new_logger

    async def init_logging(self, *args: str) -> None:
        """Initialize all available loggers"""

        if len(args) == 0:
            loggers = ["root"] + [
                lg
                for lg in logging.Logger.manager.loggerDict.keys()
                if "." not in lg or lg in args
            ]
        else:
            loggers = list(args)

        # loggers = set(loggers)

        self._logger.debug("Initializing loggers: %s", str(loggers))
        await self._init_module_loggers(*loggers)

    def info(self, msg: Any, *args: Any | None):
        self._logger.info(msg, *args)

    def error(self, msg: Any, *args: Any | None):
        self._logger.info(msg, *args)

    def warning(self, msg: Any, *args: Any | None):
        self._logger.info(msg, *args)

    def debug(self, msg: Any, *args: Any | None):
        self._logger.info(msg, *args)

    def _get_handler(self) -> logging.Handler:
        """
        Creates and returns a configured logging handler (private method).

        Returns:
            logging.Handler: A configured stream handler with proper formatting and level
        """
        formatter = LoggerFormatter()
        handler = logging.StreamHandler()
        handler.setLevel(log_level)
        handler.setFormatter(formatter)
        return handler

    async def _init_module_loggers(self, *args: str):
        """Initialize multiple loggers at once (private method)"""
        for logger_name in args:
            logger = self.get_logger(logger_name)
            logger.propagate = False


# For backwards compatibility
get_logger = Logger().get_logger
init_logging = Logger().init_logging

# For IDE and module level exports
__all__ = ["get_logger", "init_logging"]
