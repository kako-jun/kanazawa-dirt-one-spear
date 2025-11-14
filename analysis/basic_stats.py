#!/usr/bin/env python3
"""
基本統計分析スクリプト
データの概要把握と基礎統計量の算出
"""

import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json

# データベースパス
DB_PATH = Path(__file__).parent.parent / "backend" / "kanazawa_dirt_one_spear.db"


def get_connection():
    """データベース接続を取得"""
    return sqlite3.connect(DB_PATH)


def analyze_race_distribution():
    """レース開催の分布分析"""
    print("=" * 80)
    print("レース開催分布")
    print("=" * 80)

    conn = get_connection()

    # 年別レース数
    query = """
    SELECT
        strftime('%Y', date) as year,
        COUNT(*) as race_count,
        COUNT(DISTINCT date) as race_days
    FROM races
    GROUP BY strftime('%Y', date)
    ORDER BY year
    """
    df = pd.read_sql_query(query, conn)
    print("\n【年別レース数】")
    print(df.to_string(index=False))

    # 月別レース数（全期間集計）
    query = """
    SELECT
        strftime('%m', date) as month,
        COUNT(*) as race_count,
        ROUND(AVG(distance), 1) as avg_distance
    FROM races
    GROUP BY strftime('%m', date)
    ORDER BY month
    """
    df = pd.read_sql_query(query, conn)
    print("\n【月別レース数（全期間平均）】")
    print(df.to_string(index=False))

    # 距離別レース数
    query = """
    SELECT
        distance,
        COUNT(*) as race_count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM races), 2) as percentage
    FROM races
    GROUP BY distance
    ORDER BY race_count DESC
    """
    df = pd.read_sql_query(query, conn)
    print("\n【距離別レース数】")
    print(df.to_string(index=False))

    # 馬場状態別レース数
    query = """
    SELECT
        track_condition,
        COUNT(*) as race_count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM races), 2) as percentage
    FROM races
    GROUP BY track_condition
    ORDER BY race_count DESC
    """
    df = pd.read_sql_query(query, conn)
    print("\n【馬場状態別レース数】")
    print(df.to_string(index=False))

    # 天候別レース数
    query = """
    SELECT
        weather,
        COUNT(*) as race_count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM races), 2) as percentage
    FROM races
    GROUP BY weather
    ORDER BY race_count DESC
    """
    df = pd.read_sql_query(query, conn)
    print("\n【天候別レース数】")
    print(df.to_string(index=False))

    conn.close()


def analyze_horse_stats():
    """馬の統計分析"""
    print("\n" + "=" * 80)
    print("馬の統計")
    print("=" * 80)

    conn = get_connection()

    # 出走回数ランキング（上位20頭）
    query = """
    SELECT
        h.name as horse_name,
        COUNT(*) as race_count
    FROM entries e
    JOIN horses h ON e.horse_id = h.horse_id
    GROUP BY e.horse_id, h.name
    ORDER BY race_count DESC
    LIMIT 20
    """
    df = pd.read_sql_query(query, conn)
    print("\n【出走回数ランキング TOP20】")
    print(df.to_string(index=False))

    # 性別分布
    query = """
    SELECT
        gender,
        COUNT(DISTINCT horse_id) as horse_count,
        ROUND(COUNT(DISTINCT horse_id) * 100.0 / (SELECT COUNT(*) FROM horses WHERE is_runner = 1), 2) as percentage
    FROM horses
    WHERE is_runner = 1
    GROUP BY gender
    ORDER BY horse_count DESC
    """
    df = pd.read_sql_query(query, conn)
    print("\n【性別分布（出走馬のみ）】")
    print(df.to_string(index=False))

    conn.close()


def analyze_jockey_stats():
    """騎手の統計分析"""
    print("\n" + "=" * 80)
    print("騎手の統計")
    print("=" * 80)

    conn = get_connection()

    # 騎乗回数ランキング（上位20人）
    query = """
    SELECT
        j.name as jockey_name,
        COUNT(*) as ride_count
    FROM entries e
    JOIN jockeys j ON e.jockey_id = j.jockey_id
    GROUP BY e.jockey_id, j.name
    ORDER BY ride_count DESC
    LIMIT 20
    """
    df = pd.read_sql_query(query, conn)
    print("\n【騎乗回数ランキング TOP20】")
    print(df.to_string(index=False))

    conn.close()


def analyze_results_distribution():
    """結果の分布分析（着順データ）"""
    print("\n" + "=" * 80)
    print("結果分布分析")
    print("=" * 80)

    conn = get_connection()

    # 1着馬の馬番分布
    query = """
    SELECT
        r.first as horse_number,
        COUNT(*) as win_count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM results WHERE first IS NOT NULL), 2) as percentage
    FROM results r
    WHERE r.first IS NOT NULL
    GROUP BY r.first
    ORDER BY r.first
    """
    df = pd.read_sql_query(query, conn)
    print("\n【1着馬の馬番分布】")
    print(df.to_string(index=False))

    # 配当分布（3連単）
    query = """
    SELECT
        CASE
            WHEN payout_trifecta < 1000 THEN '0-999'
            WHEN payout_trifecta < 5000 THEN '1000-4999'
            WHEN payout_trifecta < 10000 THEN '5000-9999'
            WHEN payout_trifecta < 50000 THEN '10000-49999'
            WHEN payout_trifecta < 100000 THEN '50000-99999'
            ELSE '100000+'
        END as payout_range,
        COUNT(*) as count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM results WHERE payout_trifecta IS NOT NULL), 2) as percentage
    FROM results
    WHERE payout_trifecta IS NOT NULL
    GROUP BY payout_range
    ORDER BY
        CASE payout_range
            WHEN '0-999' THEN 1
            WHEN '1000-4999' THEN 2
            WHEN '5000-9999' THEN 3
            WHEN '10000-49999' THEN 4
            WHEN '50000-99999' THEN 5
            ELSE 6
        END
    """
    df = pd.read_sql_query(query, conn)
    print("\n【3連単配当分布】")
    print(df.to_string(index=False))

    # 配当の基本統計量
    query = """
    SELECT
        COUNT(*) as total_races,
        ROUND(AVG(payout_trifecta), 0) as avg_payout,
        MIN(payout_trifecta) as min_payout,
        MAX(payout_trifecta) as max_payout,
        ROUND(
            (SELECT payout_trifecta
             FROM results
             WHERE payout_trifecta IS NOT NULL
             ORDER BY payout_trifecta
             LIMIT 1 OFFSET (SELECT COUNT(*)/2 FROM results WHERE payout_trifecta IS NOT NULL)),
            0
        ) as median_payout
    FROM results
    WHERE payout_trifecta IS NOT NULL
    """
    df = pd.read_sql_query(query, conn)
    print("\n【3連単配当の基本統計量】")
    print(df.to_string(index=False))

    conn.close()


def main():
    """メイン実行関数"""
    print("金沢競馬データ基本統計分析")
    print(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"データベース: {DB_PATH}")

    analyze_race_distribution()
    analyze_horse_stats()
    analyze_jockey_stats()
    analyze_results_distribution()

    print("\n" + "=" * 80)
    print("分析完了")
    print("=" * 80)


if __name__ == "__main__":
    main()
