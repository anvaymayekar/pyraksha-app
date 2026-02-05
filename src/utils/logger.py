import logging
from pathlib import Path
from datetime import datetime
from src.config.app_config import AppConfig


class Logger:
    _loggers = {}

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        if name in cls._loggers:
            return cls._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:
            AppConfig.ensure_storage_dir()
            log_file = (
                AppConfig.STORAGE_DIR
                / f"pyraksha_{datetime.now().strftime('%Y%m%d')}.log"
            )

            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        cls._loggers[name] = logger
        return logger

    @classmethod
    def log_error(cls, name: str, message: str, exception: Exception = None):
        logger = cls.get_logger(name)
        if exception:
            logger.error(f"{message}: {str(exception)}", exc_info=True)
        else:
            logger.error(message)

    @classmethod
    def log_info(cls, name: str, message: str):
        logger = cls.get_logger(name)
        logger.info(message)

    @classmethod
    def log_warning(cls, name: str, message: str):
        logger = cls.get_logger(name)
        logger.warning(message)

    @classmethod
    def log_debug(cls, name: str, message: str):
        logger = cls.get_logger(name)
        logger.debug(message)
