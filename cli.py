import math
from typing import Any

from api_client import CurrencyAPIError, get_currency_rates
from storage import (
    DEFAULT_CACHE_PATH,
    is_cache_fresh,
    read_from_file,
    save_to_file,
)


DISPLAY_CURRENCIES = ("RUB", "EUR", "GBP")


def convert_amount(
    data: dict[str, Any], from_code: str, to_code: str, amount: float
) -> float:
    rates = data.get("rates")
    if not isinstance(rates, dict):
        raise ValueError("В данных отсутствуют курсы валют.")

    from_code = from_code.strip().upper()
    to_code = to_code.strip().upper()
    missing_codes = [code for code in (from_code, to_code) if code not in rates]
    if missing_codes:
        raise ValueError(
            f"Нет курса для валюты: {', '.join(dict.fromkeys(missing_codes))}."
        )
    if not math.isfinite(amount) or amount < 0:
        raise ValueError("Сумма должна быть конечным неотрицательным числом.")

    from_rate = rates[from_code]
    to_rate = rates[to_code]
    if (
        isinstance(from_rate, bool)
        or not isinstance(from_rate, (int, float))
        or isinstance(to_rate, bool)
        or not isinstance(to_rate, (int, float))
        or not math.isfinite(from_rate)
        or not math.isfinite(to_rate)
        or from_rate <= 0
        or to_rate <= 0
    ):
        raise ValueError("В кэше указан некорректный курс валюты.")

    return amount * to_rate / from_rate


def _load_rates(base: str) -> dict[str, Any]:
    try:
        if is_cache_fresh(DEFAULT_CACHE_PATH):
            cached_data = read_from_file(DEFAULT_CACHE_PATH)
            if (
                cached_data.get("base_code") == base
                and isinstance(cached_data.get("rates"), dict)
            ):
                print("Используются курсы из актуального кэша.")
                return cached_data
    except FileNotFoundError:
        pass
    except (OSError, ValueError) as error:
        print(f"Не удалось прочитать кэш ({error}); запрашиваю свежие данные.")

    data = get_currency_rates(base)
    try:
        save_to_file(data, DEFAULT_CACHE_PATH)
    except OSError as error:
        print(f"Не удалось сохранить кэш: {error}")
    return data


def main() -> None:
    base = input("Введите базовую валюту (например, USD): ").strip().upper()
    if not base:
        print("Код базовой валюты не может быть пустым.")
        return

    try:
        data = _load_rates(base)
    except CurrencyAPIError as error:
        print(error)
        return

    rates = data["rates"]
    print(f"Курсы относительно {data.get('base_code', base)}:")
    for code in DISPLAY_CURRENCIES:
        if code in rates:
            print(f"{code}: {rates[code]}")
        else:
            print(f"{code}: курс не предоставлен сервисом.")

    if input("Выполнить конвертацию? (д/н): ").strip().lower() not in {
        "д",
        "да",
        "y",
        "yes",
    }:
        return

    from_code = input("Из валюты: ")
    to_code = input("В валюту: ")
    try:
        amount = float(input("Сумма: "))
        result = convert_amount(data, from_code, to_code, amount)
    except ValueError as error:
        print(f"Не удалось выполнить конвертацию: {error}")
        return

    print(f"Результат: {result:.4f} {to_code.strip().upper()}")


if __name__ == "__main__":
    main()
