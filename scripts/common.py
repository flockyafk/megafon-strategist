"""Общие функции скриптов: корень репозитория и активный проект."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def active_project() -> Path | None:
    f = ROOT / ".active_project"
    if not f.exists():
        return None
    name = f.read_text(encoding="utf-8").strip()
    p = ROOT / "projects" / name
    return p if name and p.exists() else None
