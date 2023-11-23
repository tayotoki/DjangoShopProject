import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

secrets_path = BASE_DIR / "secrets" / ".secrets"

if secrets_path.exists():
    load_dotenv(secrets_path)


# Postgres
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")

# Django secrets
APP_KEY = os.getenv("APP_KEY")


class SecretsError(Exception):
    def __init__(self, message: str = "Ошибка чтения секретов. "
                                      "Создайте файл .secrets в директории /secrets. "
                                      "Пример '.secrets_example'. "
                                      "Или задайте переменные окружения: "
                                      "PG_USER, PG_PASSWORD, APP_KEY"):
        self.message = message

    def __repr__(self):
        return self.message

    __str__ = __repr__


if not all(
    (PG_PASSWORD, PG_USER, APP_KEY)
):
    raise SecretsError
