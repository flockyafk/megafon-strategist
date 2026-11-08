#!/usr/bin/env bash
# Создаёт новый проект из шаблона и делает его активным.
set -euo pipefail
cd "$(dirname "$0")/.."
name="${1:?Укажи имя проекта: bash scripts/new_project.sh <имя>}"
dir="projects/$name"
if [ -d "$dir" ]; then
  echo "Проект $dir уже есть. Делаю его активным."
else
  cp -r projects/_template "$dir"
  mkdir -p "$dir"/{output,calc,interviews,sources/web}
  printf "# Журнал действий\n\n" > "$dir/log.md"
  echo "session_id,date,model,input_tokens,output_tokens,cache_write,cache_read,usd" > "$dir/costs.csv"
  sed -i "s/^- Обновлено: .*/- Обновлено: $(date +%F)/" "$dir/state.md"
  echo "Создан $dir"
fi
echo "$name" > .active_project
