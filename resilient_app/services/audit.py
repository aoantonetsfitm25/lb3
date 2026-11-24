"""Журналювання помилок перед повторним передаванням виключення."""

from typing import NoReturn

from ..errors import AppError


def log_and_reraise(error: AppError, journal: list[str]) -> NoReturn:
    """Записує доменну помилку та повторно піднімає її без змін.

    Args:
        error (AppError): Виключення, яке потрібно передати вище.
        journal (list[str]): Список для демонстраційного журналу.

    Returns:
        NoReturn: Функція завжди завершується підняттям виключення.

    Raises:
        AppError: Повторно піднімає переданий екземпляр.
    """
    try:
        raise error
    except AppError as caught:
        journal.append(f"{caught.code}: {caught.message}")
        raise
