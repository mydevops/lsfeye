import logging
import os
from typing import Union

from loguru import logger

from lsfeye.lib.config import settings


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        """
        配置 loguru。

        Args:
            record: 记录日志
        """
        try:
            level: Union[str, int] = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def _configure_logging() -> None:
    """配置日志"""
    intercept_handler = InterceptHandler()

    logging.basicConfig(handlers=[intercept_handler], level=logging.NOTSET)

    for logger_name in logging.root.manager.loggerDict:
        if logger_name.startswith("uvicorn."):
            logging.getLogger(logger_name).handlers = []

    for _log in ["uvicorn", "uvicorn.access", "fastapi"]:
        logging.getLogger(_log).handlers = [intercept_handler]

    logger.remove()
    logger.add(
        os.path.join(settings.loguru.path, settings.loguru.filename),
        rotation=settings.loguru.rotation,
        enqueue=True,
        backtrace=True,
        level=settings.loguru.level.upper(),
        format=settings.loguru.format,
    )


def init() -> None:
    _configure_logging()
