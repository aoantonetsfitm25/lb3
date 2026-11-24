"""Публічний інтерфейс пакета resilient_app.

Пакет експортує базові доменні виключення, їх конкретні підкласи та точку
входу ``main``. Бізнес-операції розміщені в підпакеті ``services``.
"""

from .errors import AppError, BusinessRuleError, InputValidationError, RecordNotFoundError
from .cli import main

__all__ = [
    "AppError",
    "BusinessRuleError",
    "InputValidationError",
    "RecordNotFoundError",
    "main",
]
