import json
import os
from typing import Any


def load_data(filepath: str) -> list[dict[str, Any]]:
    """Загружает список сущностей из JSON-файла."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_data(filepath: str, data: list[dict[str, Any]]) -> None:
    """Сохраняет список сущностей в JSON-файл."""
    folder = os.path.dirname(filepath)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
