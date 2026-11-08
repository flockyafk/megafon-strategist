"""Хук Stop: считает токены и стоимость текущего сеанса по транскрипту Claude Code
и обновляет строку сеанса в costs.csv активного проекта.
Считает и основную модель, и субагентов, если их записи есть в транскрипте."""
import csv
import json
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import ROOT, active_project

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

p = active_project()
tpath = data.get("transcript_path")
sid = data.get("session_id", "unknown")
if p is None or not tpath or not Path(tpath).exists():
    sys.exit(0)

prices = json.loads((ROOT / "scripts" / "prices.json").read_text(encoding="utf-8"))


def price_for(model: str) -> dict:
    for key, val in prices.items():
        if not key.startswith("_") and key in model:
            return val
    return prices["sonnet"]


usage = defaultdict(lambda: defaultdict(int))
seen = set()
files = [Path(tpath)]
sub_dir = Path(tpath).with_suffix("") / "subagents"
if sub_dir.exists():
    files += list(sub_dir.glob("*.jsonl"))

for fp in files:
    for raw in fp.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            rec = json.loads(raw)
        except Exception:
            continue
        msg = rec.get("message") or {}
        u = msg.get("usage")
        if not u:
            continue
        mid = msg.get("id") or rec.get("uuid")
        if mid in seen:
            continue
        seen.add(mid)
        m = msg.get("model", "unknown")
        usage[m]["input"] += u.get("input_tokens", 0)
        usage[m]["output"] += u.get("output_tokens", 0)
        usage[m]["cache_write"] += u.get("cache_creation_input_tokens", 0)
        usage[m]["cache_read"] += u.get("cache_read_input_tokens", 0)

costs = p / "costs.csv"
rows = []
if costs.exists():
    with open(costs, encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["session_id"] != sid]

for model, u in usage.items():
    pr = price_for(model)
    usd = sum(u[k] * pr[k] for k in ("input", "output", "cache_write", "cache_read")) / 1e6
    rows.append({
        "session_id": sid, "date": date.today().isoformat(), "model": model,
        "input_tokens": u["input"], "output_tokens": u["output"],
        "cache_write": u["cache_write"], "cache_read": u["cache_read"],
        "usd": f"{usd:.4f}",
    })

fields = ["session_id", "date", "model", "input_tokens", "output_tokens", "cache_write", "cache_read", "usd"]
with open(costs, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)
