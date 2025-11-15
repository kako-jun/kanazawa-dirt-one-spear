#!/usr/bin/env python3
"""
テスト投入したデータを確認
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "backend" / "data" / "kanazawa_dirt_one_spear.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("=" * 80)
print("20241124のレースデータを確認")
print("=" * 80)

cursor.execute("""
    SELECT race_id, date, track_condition, weather
    FROM races
    WHERE race_id LIKE '20241124%'
    ORDER BY race_id
""")

print("\n【20241124のレース】")
rows = cursor.fetchall()
if rows:
    for row in rows:
        print(f"  {row[0]}: track='{row[2]}', weather='{row[3]}'")
else:
    print("  データなし")

print("\n" + "=" * 80)
print("20241124の馬の性別を確認")
print("=" * 80)

cursor.execute("""
    SELECT DISTINCT h.name, h.gender, h.age
    FROM horses h
    JOIN entries e ON h.horse_id = e.horse_id
    JOIN races r ON e.race_id = r.race_id
    WHERE r.race_id LIKE '20241124%'
    LIMIT 10
""")

print("\n【20241124に出走した馬（サンプル10頭）】")
for row in cursor.fetchall():
    gender_label = row[1] if row[1] else 'NULL'
    age_label = row[2] if row[2] else 'NULL'
    print(f"  {row[0]}: gender='{gender_label}', age={age_label}")

conn.close()
