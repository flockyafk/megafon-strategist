"""Быстрый осмотр таблицы: листы, колонки, типы, пропуски, первые строки.
Пример: python scripts/table_peek.py projects/demo/sources/data.xlsx"""
import sys
import pandas as pd

path = sys.argv[1]
sheets = pd.read_excel(path, sheet_name=None) if path.endswith((".xlsx", ".xls")) else {"csv": pd.read_csv(path)}
for name, df in sheets.items():
    print(f"\n== Лист: {name}. Строк: {len(df)}, колонок: {len(df.columns)}")
    info = pd.DataFrame({"тип": df.dtypes.astype(str), "пропуски": df.isna().sum()})
    print(info.to_string())
    print(df.head(5).to_string())
