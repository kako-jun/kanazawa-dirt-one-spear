#!/usr/bin/env python3
"""
馬場状態×距離の交互作用分析

馬場状態と距離の組み合わせが勝率に与える影響を分析
- 馬場状態別・距離別のクロス集計
- 統計的有意性の検定（カイ二乗検定）
- ヒートマップによる可視化
"""

import sqlite3
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency

# 日本語フォント設定
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# データベースパス
DB_PATH = Path(__file__).parent.parent / "backend" / "data" / "kanazawa_dirt_one_spear.db"
OUTPUT_DIR = Path(__file__).parent / "output" / "track_distance"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def get_connection():
    """データベース接続を取得"""
    return sqlite3.connect(DB_PATH)

def analyze_win_rate_by_condition_distance():
    """馬場状態×距離別の勝率分析"""
    conn = get_connection()

    print("=" * 80)
    print("馬場状態×距離の交互作用分析")
    print("=" * 80)
    print()

    print("【1. 馬場状態×距離別勝率】")
    print("-" * 80)

    # データ取得
    query = """
    SELECT
        r.track_condition,
        CASE
            WHEN r.distance <= 1200 THEN '1000-1200m'
            WHEN r.distance <= 1400 THEN '1300-1400m'
            WHEN r.distance <= 1600 THEN '1500-1600m'
            WHEN r.distance <= 1800 THEN '1700-1800m'
            WHEN r.distance <= 2000 THEN '1900-2000m'
            ELSE '2100m-'
        END as distance_category,
        COUNT(*) as total_horses,
        SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) as wins,
        ROUND(SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as win_rate
    FROM races r
    JOIN race_performances rp ON r.race_id = rp.race_id
    WHERE rp.finish_position IS NOT NULL
    GROUP BY r.track_condition, distance_category
    ORDER BY r.track_condition, distance_category
    """

    df = pd.read_sql_query(query, conn)

    if df.empty:
        print("データが見つかりませんでした")
        conn.close()
        return

    # ピボットテーブル作成（勝率）
    pivot_rate = df.pivot_table(
        index='distance_category',
        columns='track_condition',
        values='win_rate',
        fill_value=0
    )

    # ピボットテーブル作成（出走数）
    pivot_count = df.pivot_table(
        index='distance_category',
        columns='track_condition',
        values='total_horses',
        fill_value=0
    )

    # 馬場状態の順序を定義
    condition_order = ['良', '稍重', '重', '不良']
    available_conditions = [c for c in condition_order if c in pivot_rate.columns]
    pivot_rate = pivot_rate[available_conditions]
    pivot_count = pivot_count[available_conditions]

    # 距離の順序を定義
    distance_order = ['1000-1200m', '1300-1400m', '1500-1600m', '1700-1800m', '1900-2000m', '2100m-']
    available_distances = [d for d in distance_order if d in pivot_rate.index]
    pivot_rate = pivot_rate.reindex(available_distances)
    pivot_count = pivot_count.reindex(available_distances)

    print("\n勝率 (%)")
    print(pivot_rate.to_string())

    print("\n\n出走数")
    print(pivot_count.to_string())

    # CSV保存
    pivot_rate.to_csv(OUTPUT_DIR / "win_rate_by_track_distance.csv", encoding='utf-8-sig')
    pivot_count.to_csv(OUTPUT_DIR / "horse_count_by_track_distance.csv", encoding='utf-8-sig')
    print(f"\n保存: {OUTPUT_DIR / 'win_rate_by_track_distance.csv'}")
    print(f"保存: {OUTPUT_DIR / 'horse_count_by_track_distance.csv'}")

    # ヒートマップ作成（勝率）
    plt.figure(figsize=(10, 8))
    sns.heatmap(pivot_rate, annot=True, fmt='.2f', cmap='RdYlGn', center=11.5,
                vmin=8, vmax=15, cbar_kws={'label': 'Win Rate (%)'})
    plt.title('Win Rate by Track Condition and Distance', fontsize=14, pad=20)
    plt.xlabel('Track Condition', fontsize=12)
    plt.ylabel('Distance Category', fontsize=12)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'win_rate_heatmap.png', dpi=300, bbox_inches='tight')
    print(f"保存: {OUTPUT_DIR / 'win_rate_heatmap.png'}")
    plt.close()

    conn.close()
    return pivot_rate, pivot_count

def analyze_statistical_significance():
    """統計的有意性の検定"""
    conn = get_connection()

    print("\n【2. 統計的有意性検定（カイ二乗検定）】")
    print("-" * 80)

    # 馬場状態別の勝敗分布
    query_track = """
    SELECT
        r.track_condition,
        SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) as wins,
        SUM(CASE WHEN rp.finish_position > 1 THEN 1 ELSE 0 END) as losses
    FROM races r
    JOIN race_performances rp ON r.race_id = rp.race_id
    WHERE rp.finish_position IS NOT NULL
    GROUP BY r.track_condition
    """

    df_track = pd.read_sql_query(query_track, conn)

    # カイ二乗検定
    contingency_table = df_track[['wins', 'losses']].values
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)

    print(f"\n馬場状態と勝敗の独立性検定:")
    print(f"  カイ二乗値: {chi2:.2f}")
    print(f"  p値: {p_value:.6f}")
    print(f"  自由度: {dof}")

    if p_value < 0.001:
        print(f"  結論: 馬場状態は勝敗に強く影響する (p < 0.001) ★★★")
    elif p_value < 0.01:
        print(f"  結論: 馬場状態は勝敗に影響する (p < 0.01) ★★")
    elif p_value < 0.05:
        print(f"  結論: 馬場状態は勝敗に影響する (p < 0.05) ★")
    else:
        print(f"  結論: 馬場状態と勝敗に有意な関連なし (p >= 0.05)")

    # 距離別の勝敗分布
    query_distance = """
    SELECT
        CASE
            WHEN r.distance <= 1200 THEN '1000-1200m'
            WHEN r.distance <= 1400 THEN '1300-1400m'
            WHEN r.distance <= 1600 THEN '1500-1600m'
            WHEN r.distance <= 1800 THEN '1700-1800m'
            WHEN r.distance <= 2000 THEN '1900-2000m'
            ELSE '2100m-'
        END as distance_category,
        SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) as wins,
        SUM(CASE WHEN rp.finish_position > 1 THEN 1 ELSE 0 END) as losses
    FROM races r
    JOIN race_performances rp ON r.race_id = rp.race_id
    WHERE rp.finish_position IS NOT NULL
    GROUP BY distance_category
    """

    df_distance = pd.read_sql_query(query_distance, conn)

    contingency_table = df_distance[['wins', 'losses']].values
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)

    print(f"\n距離と勝敗の独立性検定:")
    print(f"  カイ二乗値: {chi2:.2f}")
    print(f"  p値: {p_value:.6f}")
    print(f"  自由度: {dof}")

    if p_value < 0.001:
        print(f"  結論: 距離は勝敗に強く影響する (p < 0.001) ★★★")
    elif p_value < 0.01:
        print(f"  結論: 距離は勝敗に影響する (p < 0.01) ★★")
    elif p_value < 0.05:
        print(f"  結論: 距離は勝敗に影響する (p < 0.05) ★")
    else:
        print(f"  結論: 距離と勝敗に有意な関連なし (p >= 0.05)")

    conn.close()

def analyze_interesting_patterns():
    """興味深いパターンの発見"""
    conn = get_connection()

    print("\n【3. 興味深いパターン】")
    print("-" * 80)

    # 最も勝率が高い組み合わせ
    query = """
    SELECT
        r.track_condition,
        CASE
            WHEN r.distance <= 1200 THEN '1000-1200m'
            WHEN r.distance <= 1400 THEN '1300-1400m'
            WHEN r.distance <= 1600 THEN '1500-1600m'
            WHEN r.distance <= 1800 THEN '1700-1800m'
            WHEN r.distance <= 2000 THEN '1900-2000m'
            ELSE '2100m-'
        END as distance_category,
        COUNT(*) as total_horses,
        SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) as wins,
        ROUND(SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as win_rate
    FROM races r
    JOIN race_performances rp ON r.race_id = rp.race_id
    WHERE rp.finish_position IS NOT NULL
    GROUP BY r.track_condition, distance_category
    HAVING total_horses >= 100
    ORDER BY win_rate DESC
    LIMIT 10
    """

    df_high = pd.read_sql_query(query, conn)

    print("\n勝率が高い組み合わせ TOP10 (100頭以上):")
    print(f"{'順位':<4} {'馬場':<6} {'距離':<15} {'出走数':>6} {'勝数':>5} {'勝率':>7}")
    print("-" * 60)

    for idx, row in df_high.iterrows():
        rank = idx + 1
        print(f"{rank:<4} {row['track_condition']:<6} {row['distance_category']:<15} "
              f"{row['total_horses']:>6} {row['wins']:>5} {row['win_rate']:>6.2f}%")

    # 最も勝率が低い組み合わせ
    query = """
    SELECT
        r.track_condition,
        CASE
            WHEN r.distance <= 1200 THEN '1000-1200m'
            WHEN r.distance <= 1400 THEN '1300-1400m'
            WHEN r.distance <= 1600 THEN '1500-1600m'
            WHEN r.distance <= 1800 THEN '1700-1800m'
            WHEN r.distance <= 2000 THEN '1900-2000m'
            ELSE '2100m-'
        END as distance_category,
        COUNT(*) as total_horses,
        SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) as wins,
        ROUND(SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as win_rate
    FROM races r
    JOIN race_performances rp ON r.race_id = rp.race_id
    WHERE rp.finish_position IS NOT NULL
    GROUP BY r.track_condition, distance_category
    HAVING total_horses >= 100
    ORDER BY win_rate ASC
    LIMIT 10
    """

    df_low = pd.read_sql_query(query, conn)

    print("\n\n勝率が低い組み合わせ TOP10 (100頭以上):")
    print(f"{'順位':<4} {'馬場':<6} {'距離':<15} {'出走数':>6} {'勝数':>5} {'勝率':>7}")
    print("-" * 60)

    for idx, row in df_low.iterrows():
        rank = idx + 1
        print(f"{rank:<4} {row['track_condition']:<6} {row['distance_category']:<15} "
              f"{row['total_horses']:>6} {row['wins']:>5} {row['win_rate']:>6.2f}%")

    # CSV保存
    df_high.to_csv(OUTPUT_DIR / "high_win_rate_combinations.csv", index=False, encoding='utf-8-sig')
    df_low.to_csv(OUTPUT_DIR / "low_win_rate_combinations.csv", index=False, encoding='utf-8-sig')
    print(f"\n保存: {OUTPUT_DIR / 'high_win_rate_combinations.csv'}")
    print(f"保存: {OUTPUT_DIR / 'low_win_rate_combinations.csv'}")

    conn.close()

def analyze_average_payout():
    """馬場×距離別の平均配当分析"""
    conn = get_connection()

    print("\n【4. 馬場×距離別の平均三連単配当】")
    print("-" * 80)

    query = """
    SELECT
        r.track_condition,
        CASE
            WHEN r.distance <= 1200 THEN '1000-1200m'
            WHEN r.distance <= 1400 THEN '1300-1400m'
            WHEN r.distance <= 1600 THEN '1500-1600m'
            WHEN r.distance <= 1800 THEN '1700-1800m'
            WHEN r.distance <= 2000 THEN '1900-2000m'
            ELSE '2100m-'
        END as distance_category,
        COUNT(*) as race_count,
        ROUND(AVG(p.payout), 0) as avg_payout,
        MIN(p.payout) as min_payout,
        MAX(p.payout) as max_payout
    FROM races r
    JOIN payouts p ON r.race_id = p.race_id
    WHERE p.payout_type = 'trifecta' AND p.payout IS NOT NULL
    GROUP BY r.track_condition, distance_category
    ORDER BY avg_payout DESC
    """

    df = pd.read_sql_query(query, conn)

    if df.empty:
        print("三連単配当データが見つかりませんでした")
        conn.close()
        return

    # ピボットテーブル作成
    pivot_payout = df.pivot_table(
        index='distance_category',
        columns='track_condition',
        values='avg_payout',
        fill_value=0
    )

    # 馬場状態の順序を定義
    condition_order = ['良', '稍重', '重', '不良']
    available_conditions = [c for c in condition_order if c in pivot_payout.columns]
    pivot_payout = pivot_payout[available_conditions]

    # 距離の順序を定義
    distance_order = ['1000-1200m', '1300-1400m', '1500-1600m', '1700-1800m', '1900-2000m', '2100m-']
    available_distances = [d for d in distance_order if d in pivot_payout.index]
    pivot_payout = pivot_payout.reindex(available_distances)

    print("\n平均三連単配当（円）")
    print(pivot_payout.to_string())

    # CSV保存
    pivot_payout.to_csv(OUTPUT_DIR / "avg_trifecta_payout.csv", encoding='utf-8-sig')
    print(f"\n保存: {OUTPUT_DIR / 'avg_trifecta_payout.csv'}")

    # ヒートマップ作成
    plt.figure(figsize=(10, 8))
    sns.heatmap(pivot_payout, annot=True, fmt='.0f', cmap='YlOrRd',
                cbar_kws={'label': 'Average Trifecta Payout (Yen)'})
    plt.title('Average Trifecta Payout by Track Condition and Distance', fontsize=14, pad=20)
    plt.xlabel('Track Condition', fontsize=12)
    plt.ylabel('Distance Category', fontsize=12)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'avg_payout_heatmap.png', dpi=300, bbox_inches='tight')
    print(f"保存: {OUTPUT_DIR / 'avg_payout_heatmap.png'}")
    plt.close()

    conn.close()

if __name__ == "__main__":
    print("馬場状態×距離の交互作用分析を開始します...\n")

    # 勝率分析
    pivot_rate, pivot_count = analyze_win_rate_by_condition_distance()

    # 統計的有意性検定
    analyze_statistical_significance()

    # 興味深いパターン
    analyze_interesting_patterns()

    # 平均配当分析
    analyze_average_payout()

    print("\n" + "=" * 80)
    print("馬場状態×距離の交互作用分析完了")
    print(f"出力ディレクトリ: {OUTPUT_DIR}")
    print("=" * 80)
