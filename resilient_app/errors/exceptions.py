"""Ієрархія предметних виключень для демонстраційного застосунку."""

from __future__ import annotations


class AppError(Exception):
    """Базове виключення для помилок предметної області.

    Args:
        message (str): Зрозумілий опис помилки.
        code (str): Стабільний машинний код помилки.

    Returns:
        None: Створює екземпляр виключення.

    Raises:
        None.
    """

    def __init__(self, message: str, code: str = "APP_ERROR") -> None:
        """Ініціалізує повідомлення та код помилки.

        Args:
            message (str): Текст для користувача або журналу.
            code (str): Короткий код категорії помилки.

        Returns:
            None: Конструктор нічого не повертає.

        Raises:
            None.
        """
        super().__init__(message)
        self.message = message
        self.code = code

    def __str__(self) -> str:
        """Повертає компактне повідомлення з кодом.

        Args:
            None.

        Returns:
            str: Код і опис помилки.

        Raises:
            None.
        """
        return f"{self.code}: {self.message}"

    def to_dict(self) -> dict[str, str]:
        """Перетворює помилку на серіалізований словник.

        Args:
            None.

        Returns:
            dict[str, str]: Тип, код і повідомлення помилки.

        Raises:
            None.
        """
        return {"type": type(self).__name__, "code": self.code, "message": self.message}


class InputValidationError(AppError):
    """Описує некоректне значення вхідного поля.

    Args:
        field (str): Назва поля, яке не пройшло перевірку.
        value (object): Початкове значення.

    Returns:
        None: Створює типізоване виключення валідації.

    Raises:
        None.
    """

    def __init__(self, field: str, value: object) -> None:
        """Зберігає поле та відхилене значення.

        Args:
            field (str): Назва поля.
            value (object): Значення, яке не вдалося перетворити або перевірити.

        Returns:
            None: Конструктор нічого не повертає.

        Raises:
            None.
        """
        self.field = field
        self.value = value
        super().__init__(f"Поле {field!r} має некоректне значення {value!r}.", "INVALID_INPUT")

    def __str__(self) -> str:
        """Форматує помилку валідації для консолі.

        Args:
            None.

        Returns:
            str: Повідомлення з назвою поля і значенням.

        Raises:
            None.
        """
        return f"{self.code}: поле {self.field!r}, значення {self.value!r}"


class RecordNotFoundError(AppError):
    """Описує відсутність потрібного запису або файлу.

    Args:
        record_id (str): Ідентифікатор відсутнього ресурсу.

    Returns:
        None: Створює типізоване виключення ресурсу.

    Raises:
        None.
    """

    def __init__(self, record_id: str) -> None:
        """Зберігає ідентифікатор ресурсу.

        Args:
            record_id (str): Шлях або ключ відсутнього запису.

        Returns:
            None: Конструктор нічого не повертає.

        Raises:
            None.
        """
        self.record_id = record_id
        super().__init__(f"Запис {record_id!r} не знайдено.", "NOT_FOUND")

    def __str__(self) -> str:
        """Повертає повідомлення про відсутній ресурс.

        Args:
            None.

        Returns:
            str: Код помилки та ідентифікатор ресурсу.

        Raises:
            None.
        """
        return f"{self.code}: ресурс {self.record_id!r} відсутній"


class BusinessRuleError(AppError):
    """Описує порушення правила бізнес-логіки або формату запису.

    Args:
        rule (str): Назва порушеного правила.
        detail (str): Додатковий контекст порушення.

    Returns:
        None: Створює типізоване виключення бізнес-правила.

    Raises:
        None.
    """

    def __init__(self, rule: str, detail: str) -> None:
        """Зберігає правило й пояснення.

        Args:
            rule (str): Коротка назва правила.
            detail (str): Значення або стан, що спричинили помилку.

        Returns:
            None: Конструктор нічого не повертає.

        Raises:
            None.
        """
        self.rule = rule
        self.detail = detail
        super().__init__(f"Порушено правило {rule!r}: {detail}", "BUSINESS_RULE")

    def __str__(self) -> str:
        """Форматує порушення бізнес-правила.

        Args:
            None.

        Returns:
            str: Код, назва правила та його контекст.

        Raises:
            None.
        """
        return f"{self.code}: {self.rule} ({self.detail})"
