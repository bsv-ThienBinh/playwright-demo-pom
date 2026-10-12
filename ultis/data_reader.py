import json
import csv
from pathlib import Path

_DATA_DIR = Path(__file__).parent.parent / "test-data"


def load_json(file_name: str) -> dict:
    with open(_DATA_DIR / file_name, encoding="utf-8") as f:
        return json.load(f)


def load_csv(file_name: str) -> list[dict]:
    with open(_DATA_DIR / file_name, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def get_user_from_json(key: str) -> dict:
    return load_json("users.json")[key]


def get_users_from_csv() -> list[dict]:
    return load_csv("users.csv")
