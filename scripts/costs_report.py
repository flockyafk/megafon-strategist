"""Сводка расходов активного проекта: по моделям и итого."""
import csv
import sys
from collections import defaultdict
sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import active_project

p = active_project()
if p is None or not (p / "costs.csv").exists():
    print("Нет данных о расходах.")
    sys.exit(0)

by_model = defaultdict(lambda: [0, 0, 0.0])
sessions = set()
with open(p / "costs.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        sessions.add(r["session_id"])
        m = by_model[r["model"]]
        m[0] += int(r["input_tokens"]) + int(r["cache_write"]) + int(r["cache_read"])
        m[1] += int(r["output_tokens"])
        m[2] += float(r["usd"])

print(f"Проект: {p.name}. Сеансов: {len(sessions)}")
print("| Модель | Вход, токены | Выход, токены | $ |")
print("|---|---|---|---|")
total = 0.0
for model, (i, o, usd) in sorted(by_model.items()):
    total += usd
    print(f"| {model} | {i:,} | {o:,} | {usd:.2f} |")
print(f"| Итого | | | {total:.2f} |")
