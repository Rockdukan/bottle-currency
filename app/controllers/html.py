import json
from datetime import datetime, timedelta

from bottle import request, template

from app import app
from app.services.parser import get_or_fetch_rate
from config import CURRENCIES


@app.get("/")
def currency_view():
    today = datetime.today().date()

    from_date = request.GET.get("from_date") or (today - timedelta(days=13)).isoformat()
    to_date = request.GET.get("to_date") or today.isoformat()

    date_from = datetime.strptime(from_date, "%Y-%m-%d").date()
    date_to = datetime.strptime(to_date, "%Y-%m-%d").date()

    # Генерация списка всех дат между from_date и to_date
    dates = [(date_from + timedelta(days=i)) for i in range((date_to - date_from).days + 1)]
    labels = [d.strftime("%d.%m") for d in dates]

    # Получаем выбранные валюты или используем все
    selected = request.GET.getall("currencies") or list(CURRENCIES.keys())

    data = {}

    # Получаем курс для каждой валюты на каждую дату
    for code in selected:
        data[code] = [get_or_fetch_rate(code, day) or 0 for day in dates]

    return template(
        "index",
        labels=json.dumps(labels),
        data=json.dumps(data),
        currencies=CURRENCIES,
        selected=selected,
        from_date=from_date,
        to_date=to_date)
