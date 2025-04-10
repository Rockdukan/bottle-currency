import json
from datetime import datetime
from unittest.mock import patch

import pytest
from bottle import template
from webtest import TestApp

from app import app
from app.controllers import html, static
from app.models.currency import CurrencyRate
from app.services.parser import fetch_rate_from_cbr, get_or_fetch_rate


@patch("app.services.parser.requests.get")
def test_fetch_rate_from_cbr_success(mock_get):
    html = """
        <table>
            <tr><td>36</td><td>USD</td><td>Доллар США</td><td>1</td><td>84,25</td></tr>
        </table>
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = html

    rate = fetch_rate_from_cbr("USD", datetime(2025, 4, 10).date())
    assert isinstance(rate, float)
    assert round(rate, 2) == 84.25


@patch("app.services.parser.requests.get")
def test_fetch_rate_from_cbr_fail(mock_get):
    mock_get.side_effect = Exception("Request failed")
    rate = fetch_rate_from_cbr("USD", datetime(2025, 4, 10).date())
    assert rate is None


def test_get_or_fetch_rate_creates_record(test_db):
    CurrencyRate.delete().execute()
    date = datetime(2025, 4, 10).date()

    with patch("app.services.parser.fetch_rate_from_cbr", return_value=84.25):
        rate = get_or_fetch_rate("USD", date)
        assert isinstance(rate, float)
        assert rate == 84.25

        # Проверка, что в БД теперь есть запись
        record = CurrencyRate.get_or_none((CurrencyRate.code == "USD") & (CurrencyRate.date == date.isoformat()))
        assert record is not None
        assert record.rate == 84.25


def test_currency_view_route(monkeypatch):
    monkeypatch.setattr("app.services.parser.get_or_fetch_rate", lambda code, date: 80.0)

    test_app = TestApp(app)
    response = test_app.get("/?currencies=USD&from_date=2025-04-01&to_date=2025-04-10")

    assert response.status_code == 200
    assert "Курс валют ЦБ РФ" in response.text
    assert '<canvas id="currencyChart"></canvas>' in response.text
