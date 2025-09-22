import logging
import logging.config
from pathlib import Path

from src.api.settings.config import config

LOGS_ROOT_DIR = Path(config.logs.root_dir)
LOGS_ROOT_DIR.mkdir(parents=True, exist_ok=True)

LOGS_ROOT_DIR = config.logs.root_dir


def setup_logging(
    level=logging.DEBUG,
    formatter: dict | None = None,
):
    if formatter is None:
        formatter = {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        }

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,  # важно: не отключаем стандартные логгеры
        "formatters": {
            "detailed": formatter,
        },
        "features": {
            "file": {
                "class": "logging.FileHandler",
                "filename": f"{LOGS_ROOT_DIR}/app.log",
                "level": logging.getLevelName(level),
                "formatter": "detailed",
            },
            "console": {
                "class": "logging.StreamHandler",
                "level": logging.getLevelName(level),
                "formatter": "detailed",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            # здесь поднимаем уровень для transitions
            "transitions.core": {
                "level": "WARNING",
                "features": [],  # можно не указывать features — он унаследует их от root
                "propagate": False,
            },
        },
        "root": {
            "features": ["file", "console"],
            "level": logging.getLevelName(level),
        },
    }

    logging.config.dictConfig(logging_config)
