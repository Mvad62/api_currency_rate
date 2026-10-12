import json
import time
from pathlib import Path
from typing import Any


DEFAULT_CACHE_PATH = "currency_rate.json"
CACHE_MAX_AGE_SECONDS = 24 * 60 * 60


def save_to_file(
    data: dict[str, Any], path: str | Path = DEFAULT_CACHE_PATH
) -> None:
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def read_from_file(path: str | Path = DEFAULT_CACHE_PATH) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("Файл кэша содержит данные в неожиданном формате.")
    return data


def is_cache_fresh(
    path: str | Path = DEFAULT_CACHE_PATH,
    max_age_seconds: int = CACHE_MAX_AGE_SECONDS,
) -> bool:
    age_seconds = time.time() - Path(path).stat().st_mtime
    return 0 <= age_seconds < max_age_seconds
