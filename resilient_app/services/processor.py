"""Перетворення вводу, читання записів і перевірка бізнес-правил."""

import json
from pathlib import Path
from typing import Any

from ..errors import BusinessRuleError, InputValidationError, RecordNotFoundError


def parse_integer(raw: str) -> int:
    """Перетворює текст на ціле число з доменним повідомленням про помилку.

    Args:
        raw (str): Початковий текст.

    Returns:
        int: Розібране ціле число.

    Raises:
        InputValidationError: Якщо текст не є цілим числом.
    """
    try:
        return int(raw)
    except ValueError as exc:
        raise InputValidationError("ціле число", raw) from exc


def lookup_setting(config: Any, key: str) -> object:
    """Повертає значення налаштування за ключем.

    Args:
        config (Any): Словник або інший об'єкт із доступом за ключем.
        key (str): Назва параметра.

    Returns:
        object: Значення параметра.

    Raises:
        KeyError: Якщо ключ відсутній.
        TypeError: Якщо об'єкт не підтримує індексацію.
    """
    return config[key]


def load_json_record(path: Path) -> dict[str, object]:
    """Читає JSON-запис у контекстному менеджері та перевіряє його формат.

    Args:
        path (Path): Шлях до JSON-файлу.

    Returns:
        dict[str, object]: Декодований об'єкт JSON.

    Raises:
        RecordNotFoundError: Якщо файл не існує.
        BusinessRuleError: Якщо JSON пошкоджений або кореневе значення не є об'єктом.
    """
    try:
        with path.open("r", encoding="utf-8") as stream:
            payload = json.load(stream)
    except FileNotFoundError as exc:
        raise RecordNotFoundError(path.name) from exc
    except json.JSONDecodeError as exc:
        raise BusinessRuleError("JSON-формат", f"{path}: {exc.msg}") from exc
    else:
        if not isinstance(payload, dict):
            raise BusinessRuleError("кореневий JSON", "очікувався об'єкт")
        print(f"else: файл {path.name} прочитано успішно")
        return payload
    finally:
        print(f"finally: обробку {path.name} завершено; with закрив файл")


def validate_amount(amount: int) -> int:
    """Перевіряє, що сума не є від'ємною.

    Args:
        amount (int): Сума в умовних одиницях.

    Returns:
        int: Перевірене значення суми.

    Raises:
        BusinessRuleError: Якщо сума від'ємна.
    """
    if amount < 0:
        raise BusinessRuleError("сума >= 0", f"отримано {amount}")
    return amount
