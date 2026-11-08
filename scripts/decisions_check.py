"""Сверка решений: просроченные обязательства и решения на отозванных сведениях."""
import csv
import re
import sys
from datetime import date
sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import active_project

p = active_project()
if p is None:
    print("Нет активного проекта.")
    sys.exit(1)

revoked = set()
ev = p / "evidence.csv"
if ev.exists():
    with open(ev, encoding="utf-8") as f:
        revoked = {r["id"] for r in csv.DictReader(f) if r.get("status") == "отозвано"}

text = (p / "decisions.md").read_text(encoding="utf-8") if (p / "decisions.md").exists() else ""
today = date.today()
current = None
overdue, stale = [], []
for line in text.splitlines():
    if line.startswith("## D"):
        current = line[3:].strip()
    m = re.match(r"- Обязательство: (.+?) \| (.+?) \| (\d{4}-\d{2}-\d{2})", line)
    if m and date.fromisoformat(m.group(3)) < today and "[x]" not in line:
        overdue.append(f"{current}: {m.group(1)} ({m.group(2)}, срок {m.group(3)})")
    for e in re.findall(r"\bE\d+\b", line):
        if e in revoked:
            stale.append(f"{current}: опирается на отозванное {e}")

print("Просрочено:", *(overdue or ["нет"]), sep="\n- ")
print("Устаревшие основания:", *(sorted(set(stale)) or ["нет"]), sep="\n- ")
