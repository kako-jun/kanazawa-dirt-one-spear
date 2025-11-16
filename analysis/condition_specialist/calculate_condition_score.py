#!/usr/bin/env python3
"""
条件適性スコア計算スクリプト
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "backend"))

from app.database import SessionLocal, DB_PATH


def calculate_condition_affinity(horse_id, track_condition, distance_category, db):
    """
    条件適性スコアを計算

    Args:
        horse_id: 馬ID
        track_condition: 馬場状態
        distance_category: 距離カテゴリ
        db: Database session

    Returns:
        condition_score: 0-1のスコア
    """
    # 馬場状態別成績
    query_track = """
    SELECT win_rate, place_rate, total_races
    FROM stat_horse_track_condition
    WHERE horse_id = ? AND track_condition = ?
    """
    track_result = db.execute(query_track, (horse_id, track_condition)).fetchone()

    if track_result is None or track_result[2] < 2:
        track_win_rate = 0.0
    else:
        track_win_rate = track_result[0]

    # 距離カテゴリ別成績
    query_distance = """
    SELECT win_rate, place_rate, total_races
    FROM stat_horse_distance_category
    WHERE horse_id = ? AND distance_category = ?
    """
    distance_result = db.execute(query_distance, (horse_id, distance_category)).fetchone()

    if distance_result is None or distance_result[2] < 2:
        distance_win_rate = 0.0
    else:
        distance_win_rate = distance_result[0]

    # 条件適性スコア
    score = 0.4 * track_win_rate + 0.4 * distance_win_rate

    return score


def analyze_all_condition_affinities():
    """全馬の条件適性を分析"""
    print("=" * 80)
    print("Condition Specialist: 条件適性スコア計算")
    print("=" * 80)
    print(f"DB: {DB_PATH}")
    print()

    db = SessionLocal()

    try:
        # 馬場状態別成績
        query = """
        SELECT
            horse_id,
            track_condition,
            win_rate,
            place_rate,
            total_races,
            avg_finish_position
        FROM stat_horse_track_condition
        WHERE total_races >= 2
        ORDER BY win_rate DESC
        """

        df_track = pd.read_sql(query, db.connection())
        print(f"✅ 馬場状態別データ取得: {len(df_track):,}件")

        # 距離カテゴリ別成績
        query_distance = """
        SELECT
            horse_id,
            distance_category,
            win_rate,
            place_rate,
            total_races,
            avg_finish_position
        FROM stat_horse_distance_category
        WHERE total_races >= 2
        ORDER BY win_rate DESC
        """

        df_distance = pd.read_sql(query_distance, db.connection())
        print(f"✅ 距離カテゴリ別データ取得: {len(df_distance):,}件")
        print()

        # 馬場状態スペシャリスト
        print("馬場状態スペシャリスト トップ20:")
        print(df_track.nlargest(20, 'win_rate')[['horse_id', 'track_condition', 'total_races', 'win_rate']])
        print()

        # 距離スペシャリスト
        print("距離スペシャリスト トップ20:")
        print(df_distance.nlargest(20, 'win_rate')[['horse_id', 'distance_category', 'total_races', 'win_rate']])
        print()

        # 保存
        output_dir = project_root / "analysis" / "output"
        output_dir.mkdir(parents=True, exist_ok=True)

        df_track.to_csv(output_dir / "condition_track_affinities.csv", index=False)
        df_distance.to_csv(output_dir / "condition_distance_affinities.csv", index=False)

        print(f"✅ 条件適性データを保存")

        return df_track, df_distance

    finally:
        db.close()


if __name__ == "__main__":
    df_track, df_distance = analyze_all_condition_affinities()

    print()
    print("=" * 80)
    print("完了")
    print("=" * 80)
