from api_client import CurrencyAPIError, get_currency_rates
from cli import main
from storage import read_from_file, save_to_file


__all__ = [
    "CurrencyAPIError",
    "get_currency_rates",
    "read_from_file",
    "save_to_file",
    "get_currency_rate",
    "main",
]


def get_currency_rate(currency_code: str) -> dict:
    """Compatibility wrapper for the original function name."""
    return get_currency_rates(currency_code)


if __name__ == "__main__":
    main()
