#!/usr/bin/env python3
"""
騎手ランキング分析

金沢競馬の騎手の成績を多角的に分析
- 基本成績（勝率、連対率、複勝率）
- 馬場状態別成績
- 距離別成績
- 回収率分析
"""

import sqlite3
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 日本語フォント設定
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# データベースパス
DB_PATH = Path(__file__).parent.parent / "backend" / "data" / "kanazawa_dirt_one_spear.db"
OUTPUT_DIR = Path(__file__).parent / "output" / "jockey_rankings"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def get_connection():
    """データベース接続を取得"""
    return sqlite3.connect(DB_PATH)

def analyze_basic_stats(min_races=50):
    """基本成績ランキング"""
    conn = get_connection()

    print("=" * 80)
    print("騎手ランキング分析")
    print("=" * 80)
    print()

    print(f"【1. 基本成績ランキング】（{min_races}走以上）")
    print("-" * 80)

    # 騎手別の基本成績を集計
    query = """
    SELECT
        j.name as jockey_name,
        COUNT(*) as total_races,
        SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) as wins,
        SUM(CASE WHEN rp.finish_position <= 2 THEN 1 ELSE 0 END) as top2,
        SUM(CASE WHEN rp.finish_position <= 3 THEN 1 ELSE 0 END) as top3,
        ROUND(SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as win_rate,
        ROUND(SUM(CASE WHEN rp.finish_position <= 2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as place_rate,
        ROUND(SUM(CASE WHEN rp.finish_position <= 3 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as show_rate,
        ROUND(AVG(CAST(rp.finish_position AS FLOAT)), 2) as avg_position
    FROM jockeys j
    JOIN entries e ON j.jockey_id = e.jockey_id
    JOIN race_performances rp ON e.entry_id = rp.entry_id
    WHERE rp.finish_position IS NOT NULL
    GROUP BY j.jockey_id, j.name
    HAVING total_races >= ?
    ORDER BY win_rate DESC, total_races DESC
    LIMIT 30
    """

    df = pd.read_sql_query(query, conn, params=(min_races,))

    if df.empty:
        print(f"データが見つかりませんでした（最小レース数: {min_races}）")
        conn.close()
        return

    # 表示
    print(f"\n{'順位':<4} {'騎手名':<20} {'騎乗数':>6} {'1着':>5} {'勝率':>7} {'連対率':>7} {'複勝率':>7} {'平均着順':>8}")
    print("-" * 80)

    for idx, row in df.iterrows():
        rank = idx + 1
        print(f"{rank:<4} {row['jockey_name']:<20} {row['total_races']:>6} {row['wins']:>5} "
              f"{row['win_rate']:>6.2f}% {row['place_rate']:>6.2f}% {row['show_rate']:>6.2f}% "
              f"{row['avg_position']:>8.2f}")

    # CSV保存
    df.to_csv(OUTPUT_DIR / "basic_rankings.csv", index=False, encoding='utf-8-sig')
    print(f"\n保存: {OUTPUT_DIR / 'basic_rankings.csv'}")

    conn.close()
    return df

def analyze_track_condition(min_races=20):
    """馬場状態別成績"""
    conn = get_connection()

    print("\n【2. 馬場状態別勝率】（各馬場{min_races}走以上）")
    print("-" * 80)

    # 馬場状態別の成績
    query = """
    SELECT
        j.name as jockey_name,
        r.track_condition,
        COUNT(*) as races,
        SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) as wins,
        ROUND(SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as win_rate
    FROM jockeys j
    JOIN entries e ON j.jockey_id = e.jockey_id
    JOIN race_performances rp ON e.entry_id = rp.entry_id
    JOIN races r ON rp.race_id = r.race_id
    WHERE rp.finish_position IS NOT NULL
    GROUP BY j.jockey_id, j.name, r.track_condition
    HAVING races >= ?
    """

    df = pd.read_sql_query(query, conn, params=(min_races,))

    if df.empty:
        print("データが見つかりませんでした")
        conn.close()
        return

    # ピボットテーブル作成
    pivot = df.pivot_table(
        index='jockey_name',
        columns='track_condition',
        values='win_rate',
        fill_value=0
    )

    # 馬場状態の順序を定義
    condition_order = ['良', '稍重', '重', '不良']
    available_conditions = [c for c in condition_order if c in pivot.columns]
    pivot = pivot[available_conditions]

    # 良馬場での成績でソート
    if '良' in pivot.columns:
        pivot = pivot.sort_values('良', ascending=False).head(20)

    print(pivot.to_string())

    # CSV保存
    pivot.to_csv(OUTPUT_DIR / "track_condition_rankings.csv", encoding='utf-8-sig')
    print(f"\n保存: {OUTPUT_DIR / 'track_condition_rankings.csv'}")

    # ヒートマップ作成
    plt.figure(figsize=(10, 12))
    sns.heatmap(pivot, annot=True, fmt='.1f', cmap='YlOrRd', cbar_kws={'label': 'Win Rate (%)'})
    plt.title('Jockey Win Rate by Track Condition', fontsize=14, pad=20)
    plt.xlabel('Track Condition', fontsize=12)
    plt.ylabel('Jockey', fontsize=12)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'track_condition_heatmap.png', dpi=300, bbox_inches='tight')
    print(f"保存: {OUTPUT_DIR / 'track_condition_heatmap.png'}")
    plt.close()

    conn.close()
    return pivot

def analyze_distance(min_races=20):
    """距離別成績"""
    conn = get_connection()

    print(f"\n【3. 距離別勝率】（各距離{min_races}走以上）")
    print("-" * 80)

    # 距離を範囲でグループ化
    query = """
    SELECT
        j.name as jockey_name,
        CASE
            WHEN r.distance <= 1400 THEN '短距離 (<=1400m)'
            WHEN r.distance <= 1700 THEN '中距離 (1500-1700m)'
            ELSE '長距離 (>=1800m)'
        END as distance_category,
        COUNT(*) as races,
        SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) as wins,
        ROUND(SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as win_rate
    FROM jockeys j
    JOIN entries e ON j.jockey_id = e.jockey_id
    JOIN race_performances rp ON e.entry_id = rp.entry_id
    JOIN races r ON rp.race_id = r.race_id
    WHERE rp.finish_position IS NOT NULL
    GROUP BY j.jockey_id, j.name, distance_category
    HAVING races >= ?
    """

    df = pd.read_sql_query(query, conn, params=(min_races,))

    if df.empty:
        print("データが見つかりませんでした")
        conn.close()
        return

    # ピボットテーブル作成
    pivot = df.pivot_table(
        index='jockey_name',
        columns='distance_category',
        values='win_rate',
        fill_value=0
    )

    # カラムの順序を定義
    distance_order = ['短距離 (<=1400m)', '中距離 (1500-1700m)', '長距離 (>=1800m)']
    available_distances = [d for d in distance_order if d in pivot.columns]
    pivot = pivot[available_distances]

    # 平均勝率でソート
    pivot['average'] = pivot.mean(axis=1)
    pivot = pivot.sort_values('average', ascending=False).head(20)
    pivot = pivot.drop('average', axis=1)

    print(pivot.to_string())

    # CSV保存
    pivot.to_csv(OUTPUT_DIR / "distance_rankings.csv", encoding='utf-8-sig')
    print(f"\n保存: {OUTPUT_DIR / 'distance_rankings.csv'}")

    # ヒートマップ作成
    plt.figure(figsize=(8, 12))
    sns.heatmap(pivot, annot=True, fmt='.1f', cmap='YlGnBu', cbar_kws={'label': 'Win Rate (%)'})
    plt.title('Jockey Win Rate by Distance Category', fontsize=14, pad=20)
    plt.xlabel('Distance Category', fontsize=12)
    plt.ylabel('Jockey', fontsize=12)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'distance_heatmap.png', dpi=300, bbox_inches='tight')
    print(f"保存: {OUTPUT_DIR / 'distance_heatmap.png'}")
    plt.close()

    conn.close()
    return pivot

def analyze_recovery_rate(min_races=50):
    """回収率分析（単勝）"""
    conn = get_connection()

    print(f"\n【4. 回収率分析】（{min_races}走以上）")
    print("-" * 80)

    # 単勝回収率を計算
    query = """
    SELECT
        j.name as jockey_name,
        COUNT(*) as total_races,
        SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) as wins,
        ROUND(SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as win_rate,
        SUM(CASE WHEN rp.finish_position = 1 THEN p.payout ELSE 0 END) as total_payout,
        ROUND(SUM(CASE WHEN rp.finish_position = 1 THEN p.payout ELSE 0 END) * 1.0 / COUNT(*), 0) as recovery_rate
    FROM jockeys j
    JOIN entries e ON j.jockey_id = e.jockey_id
    JOIN race_performances rp ON e.entry_id = rp.entry_id
    LEFT JOIN payouts p ON rp.race_id = p.race_id AND p.payout_type = 'win' AND p.combo = CAST(rp.horse_number AS TEXT)
    WHERE rp.finish_position IS NOT NULL
    GROUP BY j.jockey_id, j.name
    HAVING total_races >= ?
    ORDER BY recovery_rate DESC
    LIMIT 30
    """

    df = pd.read_sql_query(query, conn, params=(min_races,))

    if df.empty:
        print("データが見つかりませんでした")
        conn.close()
        return

    # 表示
    print(f"\n{'順位':<4} {'騎手名':<20} {'騎乗数':>6} {'勝数':>5} {'勝率':>7} {'回収率':>8}")
    print("-" * 80)

    for idx, row in df.iterrows():
        rank = idx + 1
        recovery = row['recovery_rate']
        marker = "★" if recovery >= 100 else " "
        print(f"{rank:<4} {row['jockey_name']:<20} {row['total_races']:>6} {row['wins']:>5} "
              f"{row['win_rate']:>6.2f}% {recovery:>7.0f}円 {marker}")

    # CSV保存
    df.to_csv(OUTPUT_DIR / "recovery_rate_rankings.csv", index=False, encoding='utf-8-sig')
    print(f"\n保存: {OUTPUT_DIR / 'recovery_rate_rankings.csv'}")
    print("\n★印: 回収率100%以上（理論上プラス収支）")

    conn.close()
    return df

if __name__ == "__main__":
    print("騎手ランキング分析を開始します...\n")

    # 基本成績
    df_basic = analyze_basic_stats(min_races=50)

    # 馬場状態別
    df_track = analyze_track_condition(min_races=20)

    # 距離別
    df_distance = analyze_distance(min_races=20)

    # 回収率
    df_recovery = analyze_recovery_rate(min_races=50)

    print("\n" + "=" * 80)
    print("騎手ランキング分析完了")
    print(f"出力ディレクトリ: {OUTPUT_DIR}")
    print("=" * 80)
