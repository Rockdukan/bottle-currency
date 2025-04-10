import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler


from bottle import error, request, response

from app import app
from config import (
    LOG_DIR,
    LOG_FILE,
    LOG_LEVEL,
    LOG_BACKUP_DAYS,
)


_format = "[%(asctime)s] %(levelname)s: %(message)s"
_datefmt = "%Y-%m-%d %H:%M:%S"
_formatter = logging.Formatter(_format, datefmt=_datefmt)


def setup_logger():
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger("app")
    logger.setLevel(LOG_LEVEL)
    logger.propagate = False

    file_handler = TimedRotatingFileHandler(
        LOG_FILE,
        backupCount=LOG_BACKUP_DAYS,
        encoding="utf-8",
        interval=1,
        when="midnight",
    )
    file_handler.setLevel(logging.NOTSET)
    file_handler.setFormatter(_formatter)
    logger.addHandler(file_handler)

    logging.captureWarnings(True)
    logging.getLogger().setLevel(logging.WARNING)

    return logger


logger = setup_logger()


def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    """Обработка необработанных исключений."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Необработанное исключение:", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_uncaught_exception


# Bottle-хуки и ошибки
@app.hook("before_request")
def log_request():
    logger.info(f"Запрос: {request.method} {request.url}")


@app.hook("after_request")
def log_response():
    if response.status_code >= 400:
        logger.error(f"{response.status_code} → {request.method} {request.url}")


@error(404)
def handle_404(err):
    logger.warning(f"404 Not Found: {request.url}")
    return "404 — Страница не найдена"


@error(403)
def handle_403(err):
    logger.warning(f"403 Forbidden: {request.url}")
    return "403 — Доступ запрещён"


@error(405)
def handle_405(err):
    logger.warning(f"405 Method Not Allowed: {request.method} → {request.url}")
    return "405 — Метод не поддерживается"


@error(500)
def handle_500(err):
    logger.exception("500 Internal Server Error:")
    return "500 — Внутренняя ошибка сервера"
