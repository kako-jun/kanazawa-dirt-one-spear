#!/usr/bin/env python3
"""
特徴量エンジニアリング (高速版)

ベクトル化された操作を使用して効率的に特徴量を生成する
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


def create_base_dataset():
    """
    ベースとなるデータセットを作成
    各レースの各出走馬の情報を取得
    """
    conn = get_connection()

    query = """
    SELECT
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
        r.track_condition
    FROM race_performances rp
    JOIN races r ON rp.race_id = r.race_id
    JOIN entries e ON rp.entry_id = e.entry_id
    WHERE rp.finish_position IS NOT NULL
    ORDER BY r.date, r.race_id, rp.horse_number
    """

    df = pd.read_sql_query(query, conn)
    df['race_date'] = pd.to_datetime(df['race_date'])

    # 出走頭数を計算
    horse_counts = df.groupby('race_id').size().reset_index(name='horse_count')
    df = df.merge(horse_counts, on='race_id', how='left')
    conn.close()

    print(f"Base dataset created: {len(df)} rows")
    return df


def calculate_cumulative_horse_features(df):
    """
    馬の累積特徴量を計算（ベクトル化）
    """
    print("Calculating cumulative horse features...")

    # ソート
    df = df.sort_values(['horse_id', 'race_date']).reset_index(drop=True)

    # 馬ごとにグループ化して累積統計を計算
    df['win'] = (df['finish_position'] == 1).astype(int)
    df['place'] = (df['finish_position'] <= 3).astype(int)

    grouped = df.groupby('horse_id')

    # 累積統計（shift(1)で現在のレースを除外）
    df['horse_total_races'] = grouped.cumcount()  # 0から始まるので、shift不要
    df['horse_total_wins'] = grouped['win'].cumsum().shift(1).fillna(0)
    df['horse_total_places'] = grouped['place'].cumsum().shift(1).fillna(0)
    df['horse_total_finish_sum'] = grouped['finish_position'].cumsum().shift(1).fillna(0)

    # 勝率・複勝率・平均着順
    df['horse_win_rate'] = df['horse_total_wins'] / df['horse_total_races'].replace(0, 1)
    df['horse_place_rate'] = df['horse_total_places'] / df['horse_total_races'].replace(0, 1)
    df['horse_avg_finish'] = df['horse_total_finish_sum'] / df['horse_total_races'].replace(0, 1)

    # 直近3走の平均着順（簡易版：直近1走のみ）
    df['horse_last_finish'] = grouped['finish_position'].shift(1).fillna(0)

    # 最終レースからの経過日数
    df['horse_last_race_date'] = grouped['race_date'].shift(1)
    df['horse_days_since_last_race'] = (df['race_date'] - df['horse_last_race_date']).dt.days.fillna(999)

    # 不要なカラムを削除
    df = df.drop(['win', 'place', 'horse_total_wins', 'horse_total_places',
                  'horse_total_finish_sum', 'horse_last_race_date'], axis=1)

    print(f"Horse features calculated")
    return df


def calculate_cumulative_jockey_features(df):
    """
    騎手の累積特徴量を計算（ベクトル化）
    """
    print("Calculating cumulative jockey features...")

    # ソート
    df = df.sort_values(['jockey_id', 'race_date']).reset_index(drop=True)

    # 騎手ごとにグループ化して累積統計を計算
    df['win'] = (df['finish_position'] == 1).astype(int)
    df['place'] = (df['finish_position'] <= 3).astype(int)

    grouped = df.groupby('jockey_id')

    # 累積統計
    df['jockey_total_races'] = grouped.cumcount()
    df['jockey_total_wins'] = grouped['win'].cumsum().shift(1).fillna(0)
    df['jockey_total_places'] = grouped['place'].cumsum().shift(1).fillna(0)

    # 勝率・複勝率
    df['jockey_win_rate'] = df['jockey_total_wins'] / df['jockey_total_races'].replace(0, 1)
    df['jockey_place_rate'] = df['jockey_total_places'] / df['jockey_total_races'].replace(0, 1)

    # 不要なカラムを削除
    df = df.drop(['win', 'place', 'jockey_total_wins', 'jockey_total_places'], axis=1)

    print(f"Jockey features calculated")
    return df


def calculate_cumulative_trainer_features(df):
    """
    調教師の累積特徴量を計算（ベクトル化）
    """
    print("Calculating cumulative trainer features...")

    # ソート
    df = df.sort_values(['trainer_id', 'race_date']).reset_index(drop=True)

    # 調教師ごとにグループ化して累積統計を計算
    df['win'] = (df['finish_position'] == 1).astype(int)
    df['place'] = (df['finish_position'] <= 3).astype(int)

    grouped = df.groupby('trainer_id')

    # 累積統計
    df['trainer_total_races'] = grouped.cumcount()
    df['trainer_total_wins'] = grouped['win'].cumsum().shift(1).fillna(0)
    df['trainer_total_places'] = grouped['place'].cumsum().shift(1).fillna(0)

    # 勝率・複勝率
    df['trainer_win_rate'] = df['trainer_total_wins'] / df['trainer_total_races'].replace(0, 1)
    df['trainer_place_rate'] = df['trainer_total_places'] / df['trainer_total_races'].replace(0, 1)

    # 不要なカラムを削除
    df = df.drop(['win', 'place', 'trainer_total_wins', 'trainer_total_places'], axis=1)

    print(f"Trainer features calculated")
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
    - win: 1着なら1、それ以外は0
    - place: 3着以内なら1、それ以外は0
    """
    print("Creating target variables...")

    df['target_win'] = (df['finish_position'] == 1).astype(int)
    df['target_place'] = (df['finish_position'] <= 3).astype(int)

    print(f"Target variables created")
    print(f"  Win rate: {df['target_win'].mean():.4f}")
    print(f"  Place rate: {df['target_place'].mean():.4f}")

    return df


def save_features(df, output_path):
    """特徴量をCSVとして保存"""
    print(f"Saving features to {output_path}...")
    df.to_csv(output_path, index=False)
    print(f"Features saved: {df.shape}")
    print(f"Sample columns: {list(df.columns[:20])}")


def main():
    """メイン処理"""
    print("=== Feature Engineering (Fast Version) ===\n")

    # 出力ディレクトリ作成
    output_dir = project_root / "analysis" / "output" / "features"
    output_dir.mkdir(parents=True, exist_ok=True)

    # ベースデータセット作成
    df = create_base_dataset()

    # 特徴量計算（累積統計をベクトル化）
    df = calculate_cumulative_horse_features(df)
    df = calculate_cumulative_jockey_features(df)
    df = calculate_cumulative_trainer_features(df)
    df = add_race_condition_features(df)
    df = create_target_variable(df)

    # 保存
    output_path = output_dir / "features.csv"
    save_features(df, output_path)

    print("\n=== Feature Engineering Complete ===")
    print(f"Total samples: {len(df)}")
    print(f"Feature columns: {len(df.columns)}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
