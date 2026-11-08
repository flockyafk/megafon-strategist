#!/usr/bin/env bash
# Ищет ключи и токены в файлах репозитория. Код выхода 1, если что-то найдено.
cd "$(dirname "$0")/.."
pattern='(sk-ant-[A-Za-z0-9_-]{10,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{30,}|api[_-]?key\s*[:=]\s*["'"'"'][^"'"'"']{12,})'
if grep -rEIn --exclude-dir=.git --exclude=check_secrets.sh "$pattern" . ; then
  echo "Найдены похожие на секреты строки. Убери их перед коммитом."
  exit 1
fi
echo "Секретов не найдено."
