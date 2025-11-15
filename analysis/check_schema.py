#!/usr/bin/env python3
"""
データベーススキーマ確認
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "backend" / "data" / "kanazawa_dirt_one_spear.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# テーブル一覧を取得
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("=" * 80)
print("データベーステーブル一覧")
print("=" * 80)
for table in tables:
    print(f"\n【{table[0]}】")
    cursor.execute(f"PRAGMA table_info({table[0]})")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  {col[1]:20} {col[2]:10} NULL={'OK' if col[3] == 0 else 'NG'}")

conn.close()
