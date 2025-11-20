#!/usr/bin/env python3
"""
特徴量エンジニアリング (統計テーブル活用版)

統計テーブル（stat_*）から特徴量を取得することで、
高速かつ正確な特徴量生成を実現する。
"""

import sys
import os
import sqlite3
from pathlib import Path
import pandas as pd
import numpy as np

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "backend"))

DB_PATH = project_root / "backend" / "data" / "kanazawa_dirt_one_spear.db"


def get_connection():
    """DB接続を取得"""
    return sqlite3.connect(DB_PATH)


def create_dataset_with_stats():
    """
    統計テーブルを活用してデータセットを作成

    重要:
    - その場計算は行わない
    - 統計テーブル（stat_*）から事前計算済みの値を取得
    - 時系列リークを防ぐため、as_of_dateでJOIN
    """
    conn = get_connection()

    query = """
    SELECT
        -- 基本情報
        rp.performance_id,
        rp.race_id,
        rp.horse_id,
        e.jockey_id,
        e.trainer_id,
        rp.gate_number,
        rp.horse_number,
        rp.popularity,
        rp.finish_position,
        r.date as race_date,
        r.distance,
        r.track_condition,

        -- レース規模
        (SELECT COUNT(*) FROM race_performances rp2 WHERE rp2.race_id = rp.race_id) as horse_count,

        -- 馬の累積統計（stat_horse_cumulativeから取得）
        hc.total_races as horse_total_races,
        COALESCE(hc.win_rate, 0.0) as horse_win_rate,
        COALESCE(hc.place_rate, 0.0) as horse_place_rate,
        COALESCE(hc.avg_finish_position, 8.0) as horse_avg_finish,
        COALESCE(hc.days_since_last_race, 999) as horse_days_since_last_race,

        -- 騎手の累積統計（stat_jockey_cumulativeから取得）
        jc.total_races as jockey_total_races,
        COALESCE(jc.win_rate, 0.0) as jockey_win_rate,
        COALESCE(jc.place_rate, 0.0) as jockey_place_rate,
        COALESCE(jc.avg_finish_position, 5.0) as jockey_avg_finish,

        -- 調教師の累積統計（stat_trainer_cumulativeから取得）
        tc.total_races as trainer_total_races,
        COALESCE(tc.win_rate, 0.0) as trainer_win_rate,
        COALESCE(tc.place_rate, 0.0) as trainer_place_rate

    FROM race_performances rp
    JOIN races r ON rp.race_id = r.race_id
    JOIN entries e ON rp.entry_id = e.entry_id

    -- 統計テーブルをJOIN（時系列リーク防止のため、as_of_date <= race_dateでJOIN）
    -- 直近の統計を取得（race_date以前で最も新しいas_of_date）
    LEFT JOIN stat_horse_cumulative hc ON (
        hc.horse_id = rp.horse_id
        AND hc.as_of_date = (
            SELECT MAX(as_of_date)
            FROM stat_horse_cumulative
            WHERE horse_id = rp.horse_id
            AND as_of_date < r.date
        )
    )

    LEFT JOIN stat_jockey_cumulative jc ON (
        jc.jockey_id = e.jockey_id
        AND jc.as_of_date = (
            SELECT MAX(as_of_date)
            FROM stat_jockey_cumulative
            WHERE jockey_id = e.jockey_id
            AND as_of_date < r.date
        )
    )

    LEFT JOIN stat_trainer_cumulative tc ON (
        tc.trainer_id = e.trainer_id
        AND tc.as_of_date = (
            SELECT MAX(as_of_date)
            FROM stat_trainer_cumulative
            WHERE trainer_id = e.trainer_id
            AND as_of_date < r.date
        )
    )

    WHERE rp.finish_position IS NOT NULL
    ORDER BY r.date, r.race_id, rp.horse_number
    """

    print("Loading dataset with pre-calculated statistics...")
    df = pd.read_sql_query(query, conn)
    df['race_date'] = pd.to_datetime(df['race_date'])
    conn.close()

    print(f"Dataset created: {len(df)} rows")
    print(f"Columns: {len(df.columns)}")

    # NULL値の確認
    null_counts = df.isnull().sum()
    if null_counts.sum() > 0:
        print("\nNull value counts:")
        print(null_counts[null_counts > 0])

    return df


def add_race_condition_features(df):
    """
    レース条件の特徴量を追加
    """
    print("Adding race condition features...")

    # 馬場状態をワンホットエンコーディング
    track_dummies = pd.get_dummies(df['track_condition'], prefix='track')

    # 距離をカテゴリ化
    df['distance_category'] = pd.cut(
        df['distance'],
        bins=[0, 1400, 1600, 1800, 2000, 10000],
        labels=['1300-1400m', '1500-1600m', '1700-1800m', '1900-2000m', '2100m-']
    )
    distance_dummies = pd.get_dummies(df['distance_category'], prefix='distance')

    result = pd.concat([df, track_dummies, distance_dummies], axis=1)
    print(f"Race condition features added: {result.shape}")
    return result


def create_target_variable(df):
    """
    目的変数を作成
    - target_win: 1着なら1、それ以外は0
    - target_place: 3着以内なら1、それ以外は0
    """
    print("Creating target variables...")

    df['target_win'] = (df['finish_position'] == 1).astype(int)
    df['target_place'] = (df['finish_position'] <= 3).astype(int)

    print(f"Target variables created")
    print(f"  Win rate: {df['target_win'].mean():.4f}")
    print(f"  Place rate: {df['target_place'].mean():.4f}")

    return df


def validate_features(df):
    """
    特徴量の妥当性を検証
    """
    print("\n=== Feature Validation ===")

    # 統計テーブルから取得した特徴量の確認
    stat_features = [
        'horse_total_races', 'horse_win_rate', 'horse_place_rate',
        'jockey_total_races', 'jockey_win_rate', 'jockey_place_rate',
        'trainer_total_races', 'trainer_win_rate', 'trainer_place_rate'
    ]

    for feature in stat_features:
        if feature in df.columns:
            non_null = df[feature].notna().sum()
            null_count = df[feature].isna().sum()
            print(f"{feature:30s} - Non-null: {non_null:6d}, Null: {null_count:6d}")

    # 勝率・複勝率が0-1の範囲内か確認
    rate_features = [col for col in df.columns if 'rate' in col]
    for feature in rate_features:
        if feature in df.columns:
            min_val = df[feature].min()
            max_val = df[feature].max()
            if min_val < 0 or max_val > 1:
                print(f"⚠️ WARNING: {feature} out of range [0, 1]: [{min_val:.4f}, {max_val:.4f}]")

    print("=== Validation Complete ===\n")


def save_features(df, output_path):
    """特徴量をCSVとして保存"""
    print(f"Saving features to {output_path}...")
    df.to_csv(output_path, index=False)
    print(f"Features saved: {df.shape}")
    print(f"Sample columns: {list(df.columns[:20])}")


def main():
    """メイン処理"""
    print("=== Feature Engineering (Statistics Table Version) ===\n")

    # 出力ディレクトリ作成
    output_dir = project_root / "analysis" / "output" / "features"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 統計テーブルを活用したデータセット作成
    df = create_dataset_with_stats()

    # レース条件の特徴量追加
    df = add_race_condition_features(df)

    # 目的変数作成
    df = create_target_variable(df)

    # 特徴量の妥当性検証
    validate_features(df)

    # 保存
    output_path = output_dir / "features.csv"
    save_features(df, output_path)

    print("\n=== Feature Engineering Complete ===")
    print(f"Total samples: {len(df)}")
    print(f"Feature columns: {len(df.columns)}")
    print(f"Output: {output_path}")
    print("\n重要: このCSVは統計テーブル（stat_*）から生成されています")
    print("      統計計算のミスがある場合、stat_*テーブルを再構築してください")


if __name__ == "__main__":
    main()
