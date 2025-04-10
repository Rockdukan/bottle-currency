from datetime import datetime
from typing import Union

import requests
from bs4 import BeautifulSoup

from app.log import logger
from app.models.currency import CurrencyRate


def fetch_rate_from_cbr(code: str, date: datetime.date) -> Union[float, None]:
    """
    Получает курс указанной валюты на заданную дату с сайта ЦБ РФ.

    Args:
        code (str): Код валюты (например, "USD", "EUR").
        date (datetime.date): Дата, на которую нужно получить курс.

    Returns:
        float | None: Курс валюты в рублях, если найден, иначе None.

    Raises:
        None: Все исключения обрабатываются внутри функции и логгируются.
    """
    date_str = date.strftime("%d.%m.%Y")
    url = f"https://www.cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To={date_str}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for row in soup.find_all("tr"):
            cells = row.find_all("td")

            if len(cells) >= 5 and cells[1].text.strip() == code:
                rate_text = cells[4].text.strip().replace(",", ".")
                return float(rate_text)
    except Exception as e:
        logger.error(f"Ошибка при получении курса {code} за {date}: {e}")
        return None


def get_or_fetch_rate(code: str, date: datetime.date) -> Union[float, None]:
    """
    Получает курс валюты из базы данных или с сайта ЦБ РФ,
    если курс за указанную дату не найден в кэше.

    Args:
        code (str): Код валюты (например, "USD", "EUR").
        date (datetime.date): Дата, на которую требуется курс.

    Returns:
        float | None: Курс валюты, если удалось получить, иначе None.

    Raises:
        None: Все исключения внутри функции обрабатываются (логгируются и подавляются).
    """
    date_str = date.isoformat()

    try:
        record = CurrencyRate.get_or_none(
                (CurrencyRate.code == code) & (CurrencyRate.date == date_str))

        if record:
            return record.rate

        rate = fetch_rate_from_cbr(code, date)

        if rate:
            CurrencyRate.create(code=code, date=date_str, rate=rate)

        return rate
    except Exception as e:
        logger.error(f"Ошибка при чтении/записи курса в БД: {e}")
        return None
