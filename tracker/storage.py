"""Збереження задач у JSON-файлі."""

import json
from pathlib import Path

DB_FILE = Path(__file__).resolve().parent.parent / "tasks.json"


def load_tasks():
    if not DB_FILE.exists():
        return []
    return json.loads(DB_FILE.read_text(encoding="utf-8"))


def save_tasks(tasks):
    DB_FILE.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8")
