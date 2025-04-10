import os
import tempfile

import pytest
from peewee import SqliteDatabase

from app.extensions import db as original_db
from app.models.currency import CurrencyRate


@pytest.fixture
def test_db(monkeypatch):
    temp_db = SqliteDatabase(':memory:')

    # Подменяем оригинальную БД на временную
    monkeypatch.setattr("app.extensions.db", temp_db)
    monkeypatch.setattr("app.models.currency.db", temp_db)

    temp_db.bind([CurrencyRate])
    temp_db.connect()
    temp_db.create_tables([CurrencyRate])

    yield temp_db

    temp_db.drop_tables([CurrencyRate])
    temp_db.close()
