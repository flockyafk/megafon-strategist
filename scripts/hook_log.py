"""Хук PostToolUse: пишет каждое действие агента в log.md активного проекта."""
import json
import sys
from datetime import datetime
sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import active_project

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

p = active_project()
if p is None:
    sys.exit(0)

tool = data.get("tool_name", "?")
inp = data.get("tool_input", {}) or {}
detail = (
    inp.get("file_path")
    or inp.get("url")
    or inp.get("query")
    or inp.get("command")
    or inp.get("skill")
    or inp.get("subagent_type")
    or inp.get("description")
    or ""
)
detail = str(detail).replace("\n", " ")[:160]
line = f"- {datetime.now():%Y-%m-%d %H:%M:%S} | {tool} | {detail}\n"
with open(p / "log.md", "a", encoding="utf-8") as f:
    f.write(line)
