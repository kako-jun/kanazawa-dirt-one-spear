#!/usr/bin/env python3
"""
基礎統計分析

金沢競馬データの基本的な統計情報を分析・可視化する
Phase 2の最初のステップとして、データの全体像を把握する
"""

import sqlite3
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# 日本語フォント設定
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# データベースパス
DB_PATH = Path(__file__).parent.parent / "backend" / "data" / "kanazawa_dirt_one_spear.db"
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

def get_connection():
    """データベース接続を取得"""
    return sqlite3.connect(DB_PATH)

def analyze_basic_stats():
    """基本統計情報を分析"""
    conn = get_connection()

    print("=" * 80)
    print("金沢競馬 基礎統計分析")
    print("=" * 80)
    print()

    # 1. データ規模
    print("【1. データ規模】")
    print("-" * 40)

    cursor = conn.cursor()

    # レース数
    cursor.execute("SELECT COUNT(*) FROM races")
    total_races = cursor.fetchone()[0]
    print(f"総レース数: {total_races:,}")

    # 馬数
    cursor.execute("SELECT COUNT(*) FROM horses")
    total_horses = cursor.fetchone()[0]
    print(f"登録馬数: {total_horses:,}")

    # 騎手数
    cursor.execute("SELECT COUNT(*) FROM jockeys")
    total_jockeys = cursor.fetchone()[0]
    print(f"騎手数: {total_jockeys}")

    # 調教師数
    cursor.execute("SELECT COUNT(*) FROM trainers")
    total_trainers = cursor.fetchone()[0]
    print(f"調教師数: {total_trainers}")

    # 年度範囲
    cursor.execute("SELECT MIN(SUBSTR(race_id, 1, 4)), MAX(SUBSTR(race_id, 1, 4)) FROM races")
    min_year, max_year = cursor.fetchone()
    print(f"対象期間: {min_year}年 - {max_year}年")
    print()

    # 2. レース年度別分布
    print("【2. 年度別レース数】")
    print("-" * 40)

    cursor.execute("""
        SELECT SUBSTR(race_id, 1, 4) as year, COUNT(*) as count
        FROM races
        GROUP BY year
        ORDER BY year
    """)

    year_data = cursor.fetchall()
    for year, count in year_data:
        bar = "█" * (count // 50)
        print(f"{year}: {count:4} {bar}")
    print()

    # 3. 馬場状態分布（最終確認）
    print("【3. 馬場状態分布】")
    print("-" * 40)

    cursor.execute("""
        SELECT track_condition, COUNT(*) as count,
               ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM races), 2) as percentage
        FROM races
        GROUP BY track_condition
        ORDER BY count DESC
    """)

    for condition, count, pct in cursor.fetchall():
        bar = "█" * int(pct / 2)
        print(f"{condition:4}: {count:5} ({pct:5.2f}%) {bar}")
    print()

    # 4. 天候分布
    print("【4. 天候分布】")
    print("-" * 40)

    cursor.execute("""
        SELECT weather, COUNT(*) as count,
               ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM races), 2) as percentage
        FROM races
        GROUP BY weather
        ORDER BY count DESC
    """)

    for weather, count, pct in cursor.fetchall():
        bar = "█" * int(pct / 2)
        print(f"{weather:4}: {count:5} ({pct:5.2f}%) {bar}")
    print()

    conn.close()
    print("=" * 80)
    print("基礎統計分析完了")
    print(f"出力ディレクトリ: {OUTPUT_DIR}")
    print("=" * 80)

def analyze_win_rate():
    """勝率分析（DBから直接取得）"""
    conn = get_connection()

    print("\n【5. 人気別勝率分析】")
    print("-" * 40)

    # race_performancesテーブルから人気別勝率を計算
    df = pd.read_sql_query("""
        SELECT
            popularity,
            COUNT(*) as total,
            SUM(CASE WHEN finish_position = 1 THEN 1 ELSE 0 END) as wins,
            ROUND(SUM(CASE WHEN finish_position = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as win_rate
        FROM race_performances
        WHERE popularity IS NOT NULL AND popularity <= 10
        GROUP BY popularity
        ORDER BY popularity
    """, conn)

    print(df.to_string(index=False))
    print()

    conn.close()

def analyze_gate_number():
    """枠番別分析（DBから直接取得）"""
    conn = get_connection()

    print("\n【6. 枠番別勝率分析】")
    print("-" * 40)

    # race_performancesテーブルから枠番別勝率を計算
    df = pd.read_sql_query("""
        SELECT
            gate_number,
            COUNT(*) as total,
            SUM(CASE WHEN finish_position = 1 THEN 1 ELSE 0 END) as wins,
            ROUND(SUM(CASE WHEN finish_position = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as win_rate
        FROM race_performances
        WHERE gate_number IS NOT NULL
        GROUP BY gate_number
        ORDER BY gate_number
    """, conn)

    print(df.to_string(index=False))
    print()

    conn.close()

def analyze_payouts():
    """配当分析（DBから直接取得）"""
    conn = get_connection()

    print("\n【7. 配当統計】")
    print("-" * 40)

    # 三連単配当の統計
    df_trifecta = pd.read_sql_query("""
        SELECT
            COUNT(*) as total_races,
            ROUND(AVG(payout), 0) as avg_payout,
            MIN(payout) as min_payout,
            MAX(payout) as max_payout
        FROM payouts
        WHERE payout_type = 'trifecta' AND payout IS NOT NULL
    """, conn)

    if not df_trifecta.empty and df_trifecta['total_races'].values[0] > 0:
        print("三連単配当統計:")
        print(f"  レース数: {df_trifecta['total_races'].values[0]:,}")
        print(f"  平均: {df_trifecta['avg_payout'].values[0]:,.0f}円")
        print(f"  最小: {df_trifecta['min_payout'].values[0]:,.0f}円")
        print(f"  最大: {df_trifecta['max_payout'].values[0]:,.0f}円")
        print()

    # 単勝配当の統計
    df_win = pd.read_sql_query("""
        SELECT
            COUNT(*) as total_races,
            ROUND(AVG(payout), 0) as avg_payout,
            MIN(payout) as min_payout,
            MAX(payout) as max_payout
        FROM payouts
        WHERE payout_type = 'win' AND payout IS NOT NULL
    """, conn)

    if not df_win.empty and df_win['total_races'].values[0] > 0:
        print("単勝配当統計:")
        print(f"  レース数: {df_win['total_races'].values[0]:,}")
        print(f"  平均: {df_win['avg_payout'].values[0]:,.0f}円")
        print(f"  最小: {df_win['min_payout'].values[0]:,.0f}円")
        print(f"  最大: {df_win['max_payout'].values[0]:,.0f}円")
        print()

    conn.close()

if __name__ == "__main__":
    analyze_basic_stats()
    analyze_win_rate()
    analyze_gate_number()
    analyze_payouts()
