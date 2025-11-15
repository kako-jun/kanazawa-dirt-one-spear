#!/usr/bin/env python3
"""
データベースの生データを確認
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "backend" / "data" / "kanazawa_dirt_one_spear.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("=" * 80)
print("馬場状態の実データ確認")
print("=" * 80)

cursor.execute("""
    SELECT track_condition, COUNT(*) as count
    FROM races
    GROUP BY track_condition
    ORDER BY count DESC
""")

print("\n【馬場状態の分布】")
for row in cursor.fetchall():
    print(f"  '{row[0]}': {row[1]}件")

print("\n" + "=" * 80)
print("性別の実データ確認")
print("=" * 80)

cursor.execute("""
    SELECT gender, COUNT(*) as count
    FROM horses
    WHERE is_runner = 1
    GROUP BY gender
    ORDER BY count DESC
""")

print("\n【性別の分布（出走馬のみ）】")
for row in cursor.fetchall():
    gender_label = row[0] if row[0] else 'NULL'
    print(f"  '{gender_label}': {row[1]}頭")

print("\n" + "=" * 80)
print("サンプルレースの詳細確認")
print("=" * 80)

cursor.execute("""
    SELECT race_id, date, name, track_condition, weather
    FROM races
    ORDER BY date DESC
    LIMIT 5
""")

print("\n【最新レース5件】")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}, track='{row[3]}', weather='{row[4]}'")

conn.close()
