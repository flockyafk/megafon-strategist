"""Находит выводы и решения, которые ссылаются на указанные сведения.
Пример: python scripts/impact.py E3 E7"""
import re
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import active_project

ids = [a.upper() for a in sys.argv[1:]]
if not ids:
    print("Укажи id сведений: python scripts/impact.py E3 E7")
    sys.exit(1)
p = active_project()
if p is None:
    print("Нет активного проекта.")
    sys.exit(1)

targets = list((p / "output").glob("*.md")) + [p / "decisions.md"]
found = False
for fp in targets:
    if not fp.exists():
        continue
    for n, line in enumerate(fp.read_text(encoding="utf-8").splitlines(), 1):
        for i in ids:
            if re.search(rf"\b{i}\b", line):
                found = True
                print(f"{fp.relative_to(p)}:{n} [{i}] {line.strip()[:140]}")
if not found:
    print("Ссылок на эти сведения нет.")
