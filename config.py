import logging
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "db.sqlite3")

LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")
LOG_LEVEL = logging.INFO
LOG_BACKUP_DAYS = 7
LOG_CONSOLE = True
LOG_CONSOLE_COLOR = True

TEMPLATE_DIR = os.path.join(BASE_DIR, "app", "views")

HOST = "127.0.0.1"
PORT = 8080
DEBUG = True
RELOADER = True

# Валюты: ключ — код валюты, значение — отображаемое название
CURRENCIES = {
    "USD": "Доллар США",
    "EUR": "Евро",
    "JPY": "Иены",
    "GBP": "Фунты стерлинги",
    "CNY": "Юани",
}
