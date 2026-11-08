"""Хук SessionStart: выводит в контекст состояние активного проекта.
Так новый чат продолжает работу с сохранённого места."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import active_project

p = active_project()
if p is None:
    print("Активного проекта нет. Спроси пользователя о задаче и запусти: bash scripts/new_project.sh <имя>")
    sys.exit(0)

print(f"Активный проект: {p.name}")
state = p / "state.md"
if state.exists():
    print(state.read_text(encoding="utf-8"))
ev = p / "evidence.csv"
if ev.exists():
    n = max(0, len(ev.read_text(encoding="utf-8").strip().splitlines()) - 1)
    print(f"Сведений в реестре: {n}")
print("Продолжай с шага 'Следующий шаг'. Не повторяй сделанное.")
