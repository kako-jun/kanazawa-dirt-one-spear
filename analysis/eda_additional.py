#!/usr/bin/env python3
"""
追加EDA: オッズ・欠損値・結果データの詳細確認
"""

import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# データベースパス
DB_PATH = Path(__file__).parent.parent / "backend" / "data" / "kanazawa_dirt_one_spear.db"


def get_connection():
    """データベース接続を取得"""
    return sqlite3.connect(DB_PATH)


def analyze_odds_data():
    """オッズデータの状況確認"""
    print("=" * 80)
    print("オッズデータの分析")
    print("=" * 80)

    conn = get_connection()

    # オッズデータの存在率
    query = """
    SELECT
        COUNT(*) as total_entries,
        COUNT(odds) as entries_with_odds,
        ROUND(COUNT(odds) * 100.0 / COUNT(*), 2) as percentage_with_odds,
        MIN(odds) as min_odds,
        MAX(odds) as max_odds,
        ROUND(AVG(odds), 2) as avg_odds
    FROM entries
    """
    df = pd.read_sql_query(query, conn)
    print("\n【オッズデータの概要】")
    print(df.to_string(index=False))

    # 年別オッズデータ取得状況
    query = """
    SELECT
        strftime('%Y', r.date) as year,
        COUNT(*) as total_entries,
        COUNT(e.odds) as entries_with_odds,
        ROUND(COUNT(e.odds) * 100.0 / COUNT(*), 2) as percentage
    FROM entries e
    JOIN races r ON e.race_id = r.race_id
    GROUP BY strftime('%Y', r.date)
    ORDER BY year
    """
    df = pd.read_sql_query(query, conn)
    print("\n【年別オッズデータ取得率】")
    print(df.to_string(index=False))

    # オッズ分布（オッズがあるエントリーのみ）
    query = """
    SELECT
        CASE
            WHEN odds < 2.0 THEN '1.0-1.9'
            WHEN odds < 5.0 THEN '2.0-4.9'
            WHEN odds < 10.0 THEN '5.0-9.9'
            WHEN odds < 20.0 THEN '10.0-19.9'
            WHEN odds < 50.0 THEN '20.0-49.9'
            ELSE '50.0+'
        END as odds_range,
        COUNT(*) as count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM entries WHERE odds IS NOT NULL), 2) as percentage
    FROM entries
    WHERE odds IS NOT NULL
    GROUP BY odds_range
    ORDER BY
        CASE odds_range
            WHEN '1.0-1.9' THEN 1
            WHEN '2.0-4.9' THEN 2
            WHEN '5.0-9.9' THEN 3
            WHEN '10.0-19.9' THEN 4
            WHEN '20.0-49.9' THEN 5
            ELSE 6
        END
    """
    df = pd.read_sql_query(query, conn)
    print("\n【オッズ分布】")
    print(df.to_string(index=False))

    conn.close()


def analyze_missing_data():
    """欠損値の詳細分析"""
    print("\n" + "=" * 80)
    print("欠損値の詳細分析")
    print("=" * 80)

    conn = get_connection()

    # エントリーテーブルの欠損状況
    query = """
    SELECT
        COUNT(*) as total,
        COUNT(odds) as has_odds,
        COUNT(horse_weight) as has_horse_weight,
        COUNT(weight_diff) as has_weight_diff,
        COUNT(trainer_id) as has_trainer,
        COUNT(career_record) as has_career_record,
        COUNT(best_time) as has_best_time,
        COUNT(past_results) as has_past_results,
        ROUND(COUNT(odds) * 100.0 / COUNT(*), 2) as pct_odds,
        ROUND(COUNT(horse_weight) * 100.0 / COUNT(*), 2) as pct_weight,
        ROUND(COUNT(trainer_id) * 100.0 / COUNT(*), 2) as pct_trainer
    FROM entries
    """
    df = pd.read_sql_query(query, conn)
    print("\n【エントリーデータの充実度】")
    for col in df.columns:
        val = df[col].values[0]
        print(f"  {col}: {val}")

    # 馬テーブルの欠損状況
    query = """
    SELECT
        COUNT(*) as total_horses,
        COUNT(birth_date) as has_birth_date,
        COUNT(age) as has_age,
        COUNT(gender) as has_gender,
        COUNT(sire_id) as has_sire,
        COUNT(dam_id) as has_dam,
        ROUND(COUNT(birth_date) * 100.0 / COUNT(*), 2) as pct_birth_date,
        ROUND(COUNT(age) * 100.0 / COUNT(*), 2) as pct_age,
        ROUND(COUNT(gender) * 100.0 / COUNT(*), 2) as pct_gender
    FROM horses
    WHERE is_runner = 1
    """
    df = pd.read_sql_query(query, conn)
    print("\n【馬データの充実度（出走馬のみ）】")
    for col in df.columns:
        val = df[col].values[0]
        print(f"  {col}: {val}")

    conn.close()


def analyze_results_data():
    """結果データの分析"""
    print("\n" + "=" * 80)
    print("結果データの分析")
    print("=" * 80)

    conn = get_connection()

    # 結果データの存在率
    query = """
    SELECT
        (SELECT COUNT(*) FROM races) as total_races,
        COUNT(*) as races_with_results,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM races), 2) as percentage_with_results
    FROM results
    """
    df = pd.read_sql_query(query, conn)
    print("\n【結果データの存在率】")
    print(df.to_string(index=False))

    # 結果データの詳細
    query = """
    SELECT
        COUNT(*) as total_results,
        COUNT(first) as has_first,
        COUNT(second) as has_second,
        COUNT(third) as has_third,
        COUNT(finish_order) as has_finish_order,
        COUNT(payout_trifecta) as has_payout_trifecta,
        COUNT(corner_positions) as has_corner_positions,
        ROUND(COUNT(first) * 100.0 / COUNT(*), 2) as pct_first,
        ROUND(COUNT(payout_trifecta) * 100.0 / COUNT(*), 2) as pct_payout
    FROM results
    """
    df = pd.read_sql_query(query, conn)
    print("\n【結果データの充実度】")
    for col in df.columns:
        val = df[col].values[0]
        print(f"  {col}: {val}")

    # 年別結果データ取得状況
    query = """
    SELECT
        strftime('%Y', r.date) as year,
        COUNT(DISTINCT r.race_id) as total_races,
        COUNT(DISTINCT res.race_id) as races_with_results,
        ROUND(COUNT(DISTINCT res.race_id) * 100.0 / COUNT(DISTINCT r.race_id), 2) as percentage
    FROM races r
    LEFT JOIN results res ON r.race_id = res.race_id
    GROUP BY strftime('%Y', r.date)
    ORDER BY year
    """
    df = pd.read_sql_query(query, conn)
    print("\n【年別結果データ取得率】")
    print(df.to_string(index=False))

    conn.close()


def analyze_data_quality_issues():
    """データ品質問題の詳細確認"""
    print("\n" + "=" * 80)
    print("データ品質問題の詳細確認")
    print("=" * 80)

    conn = get_connection()

    # 馬場状態の実データを確認
    query = """
    SELECT
        track_condition,
        COUNT(*) as count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM races), 2) as percentage
    FROM races
    GROUP BY track_condition
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    print("\n【馬場状態の分布（現状）】")
    print(df.to_string(index=False))

    # 性別の実データを確認
    query = """
    SELECT
        gender,
        COUNT(*) as count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM horses WHERE is_runner = 1), 2) as percentage
    FROM horses
    WHERE is_runner = 1
    GROUP BY gender
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    print("\n【性別の分布（現状、出走馬のみ）】")
    print(df.to_string(index=False))

    # 実際の値をサンプル表示
    query = """
    SELECT
        r.date,
        r.name as race_name,
        r.track_condition,
        r.weather
    FROM races r
    ORDER BY r.date DESC
    LIMIT 10
    """
    df = pd.read_sql_query(query, conn)
    print("\n【最新レースのサンプル（馬場状態・天候）】")
    print(df.to_string(index=False))

    query = """
    SELECT
        h.name as horse_name,
        h.gender,
        h.age,
        COUNT(e.entry_id) as race_count
    FROM horses h
    JOIN entries e ON h.horse_id = e.horse_id
    WHERE h.is_runner = 1
    GROUP BY h.horse_id
    ORDER BY race_count DESC
    LIMIT 10
    """
    df = pd.read_sql_query(query, conn)
    print("\n【出走回数上位馬のサンプル（性別確認）】")
    print(df.to_string(index=False))

    conn.close()


def main():
    """メイン実行関数"""
    print("金沢競馬データ 追加EDA")
    print(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"データベース: {DB_PATH}")
    print()

    analyze_odds_data()
    analyze_missing_data()
    analyze_results_data()
    analyze_data_quality_issues()

    print("\n" + "=" * 80)
    print("追加EDA完了")
    print("=" * 80)


if __name__ == "__main__":
    main()
