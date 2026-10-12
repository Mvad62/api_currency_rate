from typing import Any

import requests


class CurrencyAPIError(Exception):
    """Raised when the exchange-rate API cannot provide valid rates."""


def get_currency_rates(base: str) -> dict[str, Any]:
    base = base.strip().upper()
    if not base:
        raise CurrencyAPIError("Код базовой валюты не может быть пустым.")

    try:
        response = requests.get(
            f"https://open.er-api.com/v6/latest/{base}", timeout=10
        )
    except requests.RequestException as error:
        raise CurrencyAPIError(
            f"Не удалось подключиться к сервису курсов валют: {error}"
        ) from error

    if response.status_code != 200:
        raise CurrencyAPIError(
            f"Сервис курсов валют вернул HTTP {response.status_code}."
        )

    try:
        data = response.json()
    except ValueError as error:
        raise CurrencyAPIError("Сервис вернул некорректный JSON.") from error

    if not isinstance(data, dict):
        raise CurrencyAPIError("Сервис вернул данные в неожиданном формате.")
    if data.get("result") != "success":
        error_type = data.get("error-type", "неизвестная ошибка")
        raise CurrencyAPIError(f"Не удалось получить курсы валют: {error_type}.")
    if not isinstance(data.get("rates"), dict):
        raise CurrencyAPIError("В ответе сервиса отсутствует список курсов.")

    return data
