#!/usr/bin/env python3
"""
特徴量エンジニアリング

レース予想に必要な特徴量をDBから生成する
- 馬の過去成績
- 騎手の成績
- 調教師の成績
- レース条件
- 人気（オッズ情報）
"""

import sys
import os
import sqlite3
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

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


def calculate_horse_features(df):
    """
    馬の特徴量を計算
    各レース時点での過去成績を計算（未来のデータを含まないように）
    """
    print("Calculating horse features...")

    # ソート（重要：日付順に処理）
    df = df.sort_values(['horse_id', 'race_date']).reset_index(drop=True)

    horse_features = []

    for idx, row in df.iterrows():
        if idx % 1000 == 0:
            print(f"  Processing {idx}/{len(df)}...")

        horse_id = row['horse_id']
        race_date = row['race_date']
        track_condition = row['track_condition']
        distance = row['distance']

        # このレースより前のデータのみを使用
        past_races = df[
            (df['horse_id'] == horse_id) &
            (df['race_date'] < race_date)
        ]

        if len(past_races) == 0:
            # 初出走の場合
            features = {
                'horse_total_races': 0,
                'horse_win_rate': 0.0,
                'horse_place_rate': 0.0,
                'horse_avg_finish': 0.0,
                'horse_recent3_avg_finish': 0.0,
                'horse_track_win_rate': 0.0,
                'horse_distance_win_rate': 0.0,
                'horse_days_since_last_race': 999
            }
        else:
            total_races = len(past_races)
            wins = len(past_races[past_races['finish_position'] == 1])
            places = len(past_races[past_races['finish_position'] <= 3])

            # 馬場状態別成績
            track_races = past_races[past_races['track_condition'] == track_condition]
            track_wins = len(track_races[track_races['finish_position'] == 1])

            # 距離別成績（±100m範囲）
            distance_races = past_races[
                (past_races['distance'] >= distance - 100) &
                (past_races['distance'] <= distance + 100)
            ]
            distance_wins = len(distance_races[distance_races['finish_position'] == 1])

            # 直近3走の平均着順
            recent3 = past_races.tail(3)
            recent3_avg = recent3['finish_position'].mean() if len(recent3) > 0 else 0.0

            # 最終レースからの経過日数
            last_race_date = past_races['race_date'].max()
            days_since = (race_date - last_race_date).days

            features = {
                'horse_total_races': total_races,
                'horse_win_rate': wins / total_races if total_races > 0 else 0.0,
                'horse_place_rate': places / total_races if total_races > 0 else 0.0,
                'horse_avg_finish': past_races['finish_position'].mean(),
                'horse_recent3_avg_finish': recent3_avg,
                'horse_track_win_rate': track_wins / len(track_races) if len(track_races) > 0 else 0.0,
                'horse_distance_win_rate': distance_wins / len(distance_races) if len(distance_races) > 0 else 0.0,
                'horse_days_since_last_race': days_since
            }

        horse_features.append(features)

    horse_features_df = pd.DataFrame(horse_features)
    print(f"Horse features calculated: {horse_features_df.shape}")
    return pd.concat([df.reset_index(drop=True), horse_features_df], axis=1)


def calculate_jockey_features(df):
    """
    騎手の特徴量を計算
    各レース時点での過去成績を計算
    """
    print("Calculating jockey features...")

    df = df.sort_values(['jockey_id', 'race_date']).reset_index(drop=True)

    jockey_features = []

    for idx, row in df.iterrows():
        if idx % 1000 == 0:
            print(f"  Processing {idx}/{len(df)}...")

        jockey_id = row['jockey_id']
        race_date = row['race_date']
        track_condition = row['track_condition']
        distance = row['distance']

        # このレースより前のデータのみを使用
        past_races = df[
            (df['jockey_id'] == jockey_id) &
            (df['race_date'] < race_date)
        ]

        if len(past_races) == 0:
            features = {
                'jockey_total_races': 0,
                'jockey_win_rate': 0.0,
                'jockey_place_rate': 0.0,
                'jockey_track_win_rate': 0.0,
                'jockey_distance_win_rate': 0.0
            }
        else:
            total_races = len(past_races)
            wins = len(past_races[past_races['finish_position'] == 1])
            places = len(past_races[past_races['finish_position'] <= 3])

            # 馬場状態別成績
            track_races = past_races[past_races['track_condition'] == track_condition]
            track_wins = len(track_races[track_races['finish_position'] == 1])

            # 距離別成績（±100m範囲）
            distance_races = past_races[
                (past_races['distance'] >= distance - 100) &
                (past_races['distance'] <= distance + 100)
            ]
            distance_wins = len(distance_races[distance_races['finish_position'] == 1])

            features = {
                'jockey_total_races': total_races,
                'jockey_win_rate': wins / total_races if total_races > 0 else 0.0,
                'jockey_place_rate': places / total_races if total_races > 0 else 0.0,
                'jockey_track_win_rate': track_wins / len(track_races) if len(track_races) > 0 else 0.0,
                'jockey_distance_win_rate': distance_wins / len(distance_races) if len(distance_races) > 0 else 0.0
            }

        jockey_features.append(features)

    jockey_features_df = pd.DataFrame(jockey_features)
    print(f"Jockey features calculated: {jockey_features_df.shape}")
    return pd.concat([df.reset_index(drop=True), jockey_features_df], axis=1)


def calculate_trainer_features(df):
    """
    調教師の特徴量を計算
    各レース時点での過去成績を計算
    """
    print("Calculating trainer features...")

    df = df.sort_values(['trainer_id', 'race_date']).reset_index(drop=True)

    trainer_features = []

    for idx, row in df.iterrows():
        if idx % 1000 == 0:
            print(f"  Processing {idx}/{len(df)}...")

        trainer_id = row['trainer_id']
        race_date = row['race_date']
        track_condition = row['track_condition']

        # このレースより前のデータのみを使用
        past_races = df[
            (df['trainer_id'] == trainer_id) &
            (df['race_date'] < race_date)
        ]

        if len(past_races) == 0:
            features = {
                'trainer_total_races': 0,
                'trainer_win_rate': 0.0,
                'trainer_place_rate': 0.0,
                'trainer_track_win_rate': 0.0
            }
        else:
            total_races = len(past_races)
            wins = len(past_races[past_races['finish_position'] == 1])
            places = len(past_races[past_races['finish_position'] <= 3])

            # 馬場状態別成績
            track_races = past_races[past_races['track_condition'] == track_condition]
            track_wins = len(track_races[track_races['finish_position'] == 1])

            features = {
                'trainer_total_races': total_races,
                'trainer_win_rate': wins / total_races if total_races > 0 else 0.0,
                'trainer_place_rate': places / total_races if total_races > 0 else 0.0,
                'trainer_track_win_rate': track_wins / len(track_races) if len(track_races) > 0 else 0.0
            }

        trainer_features.append(features)

    trainer_features_df = pd.DataFrame(trainer_features)
    print(f"Trainer features calculated: {trainer_features_df.shape}")
    return pd.concat([df.reset_index(drop=True), trainer_features_df], axis=1)


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
    - finish_position: 着順そのまま
    """
    print("Creating target variables...")

    df['target_win'] = (df['finish_position'] == 1).astype(int)
    df['target_place'] = (df['finish_position'] <= 3).astype(int)
    df['target_finish_position'] = df['finish_position']

    print(f"Target variables created")
    print(f"  Win rate: {df['target_win'].mean():.4f}")
    print(f"  Place rate: {df['target_place'].mean():.4f}")

    return df


def save_features(df, output_path):
    """特徴量をCSVとして保存"""
    print(f"Saving features to {output_path}...")
    df.to_csv(output_path, index=False)
    print(f"Features saved: {df.shape}")
    print(f"Columns: {list(df.columns)}")


def main():
    """メイン処理"""
    print("=== Feature Engineering ===\n")

    # 出力ディレクトリ作成
    output_dir = project_root / "analysis" / "output" / "features"
    output_dir.mkdir(parents=True, exist_ok=True)

    # ベースデータセット作成
    df = create_base_dataset()

    # 特徴量計算
    df = calculate_horse_features(df)
    df = calculate_jockey_features(df)
    df = calculate_trainer_features(df)
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
