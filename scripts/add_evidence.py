"""Добавляет строку в evidence.csv активного проекта с правильным экранированием и следующим id.
Пример:
python scripts/add_evidence.py --claim "Выручка 54 млрд" --status факт --source https://... --type сайт --date 2026-07-29 --conf средняя --used research --note "J&Partners"
"""
import argparse
import csv
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import active_project

STATUSES = {"факт", "гипотеза", "прогноз", "синтетика", "отозвано"}
FIELDS = ["id", "claim", "status", "source", "source_type", "date", "confidence", "used_in", "note"]

ap = argparse.ArgumentParser()
ap.add_argument("--claim", required=True)
ap.add_argument("--status", required=True)
ap.add_argument("--source", required=True)
ap.add_argument("--type", default="сайт")
ap.add_argument("--date", default="н/д")
ap.add_argument("--conf", default="средняя")
ap.add_argument("--used", default="")
ap.add_argument("--note", default="")
a = ap.parse_args()

if a.status not in STATUSES:
    sys.exit(f"Статус должен быть одним из: {', '.join(sorted(STATUSES))}")
p = active_project()
if p is None:
    sys.exit("Нет активного проекта.")

path = p / "evidence.csv"
with open(path, encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
nums = [int(r["id"][1:]) for r in rows if r.get("id", "").startswith("E") and r["id"][1:].isdigit()]
new_id = f"E{max(nums, default=0) + 1}"

with open(path, "a", encoding="utf-8", newline="") as f:
    csv.DictWriter(f, fieldnames=FIELDS).writerow({
        "id": new_id, "claim": a.claim, "status": a.status, "source": a.source,
        "source_type": a.type, "date": a.date, "confidence": a.conf,
        "used_in": a.used, "note": a.note,
    })
print(new_id)
