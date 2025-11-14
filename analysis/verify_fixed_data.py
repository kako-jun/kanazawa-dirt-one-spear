#!/usr/bin/env python3
"""
データ修正後の最終検証
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "backend" / "data" / "kanazawa_dirt_one_spear.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("=" * 80)
print("データ修正後の最終検証")
print("=" * 80)

# 1. 馬場状態の分布確認
print("\n【1. 馬場状態の分布】")
cursor.execute("""
    SELECT track_condition, COUNT(*) as count,
           ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM races), 2) as percentage
    FROM races
    GROUP BY track_condition
    ORDER BY count DESC
""")
print("\n馬場状態 | 件数 | 割合")
print("-" * 40)
for row in cursor.fetchall():
    print(f"{row[0]:8} | {row[1]:5} | {row[2]:5}%")

# 2. 天候の分布確認
print("\n【2. 天候の分布】")
cursor.execute("""
    SELECT weather, COUNT(*) as count,
           ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM races), 2) as percentage
    FROM races
    GROUP BY weather
    ORDER BY count DESC
""")
print("\n天候 | 件数 | 割合")
print("-" * 40)
for row in cursor.fetchall():
    print(f"{row[0]:4} | {row[1]:5} | {row[2]:5}%")

# 3. 性別の分布確認
print("\n【3. 馬の性別分布】")
cursor.execute("""
    SELECT gender, COUNT(*) as count,
           ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM horses), 2) as percentage
    FROM horses
    GROUP BY gender
    ORDER BY count DESC
""")
print("\n性別 | 件数 | 割合")
print("-" * 40)
for row in cursor.fetchall():
    gender_label = row[0] if row[0] else 'NULL'
    print(f"{gender_label:6} | {row[1]:5} | {row[2]:5}%")

# 4. 年齢データの完全性確認
print("\n【4. 馬の年齢データ】")
cursor.execute("""
    SELECT
        COUNT(*) as total,
        SUM(CASE WHEN age IS NOT NULL THEN 1 ELSE 0 END) as has_age,
        ROUND(SUM(CASE WHEN age IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as age_rate
    FROM horses
""")
row = cursor.fetchone()
print(f"\n総馬数: {row[0]}")
print(f"年齢データあり: {row[1]} ({row[2]}%)")

# 5. 配当データの完全性確認
print("\n【5. 配当データの完全性】")
cursor.execute("""
    SELECT
        COUNT(*) as total_results,
        SUM(CASE WHEN payouts IS NOT NULL THEN 1 ELSE 0 END) as has_payouts,
        ROUND(SUM(CASE WHEN payouts IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as payouts_rate,
        SUM(CASE WHEN payout_trifecta IS NOT NULL THEN 1 ELSE 0 END) as has_trifecta,
        ROUND(SUM(CASE WHEN payout_trifecta IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as trifecta_rate
    FROM results
""")
row = cursor.fetchone()
print(f"\n総結果数: {row[0]}")
print(f"配当データ(JSON): {row[1]} ({row[2]}%)")
print(f"3連単配当: {row[3]} ({row[4]}%)")

# 6. サンプルデータ確認（20241124のレース）
print("\n【6. サンプルデータ確認（20241124）】")
cursor.execute("""
    SELECT race_id, track_condition, weather
    FROM races
    WHERE race_id LIKE '20241124%'
    ORDER BY race_id
    LIMIT 5
""")
print("\nrace_id | 馬場 | 天候")
print("-" * 40)
for row in cursor.fetchall():
    print(f"{row[0]} | {row[1]:4} | {row[2]:2}")

# 7. サンプル馬の性別・年齢確認（20241124）
print("\n【7. サンプル馬データ（20241124出走馬）】")
cursor.execute("""
    SELECT DISTINCT h.name, h.gender, h.age
    FROM horses h
    JOIN entries e ON h.horse_id = e.horse_id
    JOIN races r ON e.race_id = r.race_id
    WHERE r.race_id LIKE '20241124%'
    LIMIT 10
""")
print("\n馬名 | 性別 | 年齢")
print("-" * 40)
for row in cursor.fetchall():
    name = row[0]
    gender = row[1] if row[1] else 'NULL'
    age = row[2] if row[2] else 'NULL'
    print(f"{name:20} | {gender:4} | {age}")

print("\n" + "=" * 80)
print("検証完了")
print("=" * 80)

conn.close()
