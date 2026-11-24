"""Консольна демонстрація сценаріїв обробки помилок та інтроспекції API."""

from contextlib import redirect_stdout
import io
import tempfile
from pathlib import Path
from typing import Sequence

import resilient_app.services.processor as processor
from resilient_app.errors import AppError, BusinessRuleError, InputValidationError, RecordNotFoundError
from resilient_app.services.audit import log_and_reraise


def run_demo() -> None:
    """Послідовно демонструє сценарії успіху, помилок і документації.

    Args:
        None.

    Returns:
        None: Результати друкуються в консоль.

    Raises:
        None: Очікувані доменні помилки перехоплюються в демонстрації.
    """
    print("СЦЕНАРІЙ 1 — try/except для перетворення числа")
    try:
        print(f"Успіх: {processor.parse_integer('27')}")
        processor.parse_integer("двадцять")
    except InputValidationError as exc:
        print(f"Помилковий шлях: {exc}")
        print(f"Первинна причина: {type(exc.__cause__).__name__}")

    print("\nСЦЕНАРІЙ 2 — except (KeyError, TypeError)")
    for config, key in [({"theme": "dark"}, "theme"), ({}, "theme"), (None, "theme")]:
        try:
            print(f"Успіх: {processor.lookup_setting(config, key)}")
        except (KeyError, TypeError) as exc:
            print(f"Очікувана помилка {type(exc).__name__}: {exc}")

    print("\nСЦЕНАРІЙ 3 — with + try/except/else/finally")
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "record.json"
        path.write_text('{"id": 7, "status": "ready"}', encoding="utf-8")
        print(f"Успішний результат: {processor.load_json_record(path)}")
        missing = Path(folder) / "missing.json"
        journal: list[str] = []
        try:
            try:
                processor.load_json_record(missing)
            except AppError as exc:
                log_and_reraise(exc, journal)
        except RecordNotFoundError as exc:
            print(f"Перехоплено конкретний тип: {exc}")
            print(f"Причина через __cause__: {type(exc.__cause__).__name__}")
        print(f"Журнал після повторного raise: {journal}")

    print("\nСЦЕНАРІЙ 4 — перехоплення категорії AppError")
    try:
        processor.validate_amount(-5)
    except AppError as exc:
        print(f"Базовий клас перехопив {type(exc).__name__}: {exc}")
        print(f"to_dict(): {exc.to_dict()}")
    try:
        raise BusinessRuleError("статус", "перехід заборонений")
    except BusinessRuleError as exc:
        print(f"Конкретний клас перехопив: {exc}")

    print("\nСЦЕНАРІЙ 5 — __all__ та інтроспекція")
    namespace: dict[str, object] = {}
    exec("from resilient_app import *", namespace)
    names = sorted(name for name in namespace if not name.startswith("__"))
    print(f"Імена з __all__: {names}")
    help_output = io.StringIO()
    with redirect_stdout(help_output):
        help(processor.parse_integer)
    print("help(parse_integer):")
    print("\n".join(help_output.getvalue().splitlines()[:7]))
    print(f"__doc__: {processor.parse_integer.__doc__.splitlines()[0]}")
    print(f"__name__: {processor.parse_integer.__name__}")
    print(f"__annotations__: {processor.parse_integer.__annotations__}")


def main(argv: Sequence[str] | None = None) -> int:
    """Запускає консольну демонстрацію.

    Args:
        argv (Sequence[str] | None): Зарезервований список аргументів командного рядка.

    Returns:
        int: Код завершення програми, нуль у разі успіху.

    Raises:
        None: Очікувані сценарії помилок обробляються функцією ``run_demo``.
    """
    del argv
    run_demo()
    return 0
