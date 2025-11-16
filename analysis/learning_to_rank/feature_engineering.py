#!/usr/bin/env python3
"""
Learning to Rank用の特徴量エンジニアリング

LightGBM Rankerに必要なデータ形式:
- group_id (race_id): レースごとにグループ化
- features: 各馬の特徴量
- target: 順位（1, 2, 3, ..., 8）
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "backend"))

from app.database import SessionLocal, DB_PATH


def extract_features_for_ranking():
    """
    Ranking学習用の特徴量を抽出

    Returns:
        DataFrame with columns:
        - race_id (group_id)
        - horse_id
        - rank (target: 1, 2, 3, ...)
        - features...
    """
    print("=" * 80)
    print("Learning to Rank: 特徴量エンジニアリング")
    print("=" * 80)
    print(f"DB: {DB_PATH}")
    print()

    db = SessionLocal()

    try:
        # SQL: レースごとの馬の成績と統計を結合
        query = """
        SELECT
            r.id as race_id,
            r.race_date,
            r.track_condition,
            r.distance,
            CASE
                WHEN r.distance <= 1400 THEN '短距離'
                WHEN r.distance <= 1600 THEN 'マイル'
                WHEN r.distance <= 2000 THEN '中距離'
                ELSE '長距離'
            END as distance_category,

            rp.horse_id,
            rp.jockey_id,
            rp.trainer_id,
            rp.finish_position as rank,  -- ターゲット
            rp.popularity,
            rp.gate_number,
            rp.horse_number,

            -- 馬の累積統計
            sh.total_races as horse_total_races,
            sh.win_rate as horse_win_rate,
            sh.place_rate as horse_place_rate,
            sh.avg_finish_position as horse_avg_finish,

            -- 騎手の累積統計
            sj.total_races as jockey_total_races,
            sj.win_rate as jockey_win_rate,
            sj.place_rate as jockey_place_rate,

            -- 調教師の累積統計
            st.total_races as trainer_total_races,
            st.win_rate as trainer_win_rate,
            st.place_rate as trainer_place_rate

        FROM race_performances rp
        JOIN races r ON rp.race_id = r.id
        LEFT JOIN stat_horse_cumulative sh ON rp.horse_id = sh.horse_id
        LEFT JOIN stat_jockey_cumulative sj ON rp.jockey_id = sj.jockey_id
        LEFT JOIN stat_trainer_cumulative st ON rp.trainer_id = st.trainer_id
        WHERE rp.finish_position IS NOT NULL
        ORDER BY r.race_date, rp.race_id, rp.finish_position
        """

        df = pd.read_sql(query, db.connection())
        print(f"✅ データ取得完了: {len(df):,}件")
        print(f"   レース数: {df['race_id'].nunique():,}件")
        print(f"   期間: {df['race_date'].min()} 〜 {df['race_date'].max()}")
        print()

        # 欠損値を0で埋める
        df = df.fillna(0)

        # カテゴリカル変数のエンコーディング
        df['track_condition_code'] = pd.Categorical(df['track_condition']).codes
        df['distance_category_code'] = pd.Categorical(df['distance_category']).codes

        # 特徴量カラムを定義
        feature_columns = [
            'track_condition_code',
            'distance',
            'distance_category_code',
            'popularity',
            'gate_number',
            'horse_number',
            'horse_total_races',
            'horse_win_rate',
            'horse_place_rate',
            'horse_avg_finish',
            'jockey_total_races',
            'jockey_win_rate',
            'jockey_place_rate',
            'trainer_total_races',
            'trainer_win_rate',
            'trainer_place_rate',
        ]

        # group_id用のrace_idを保持
        df['group_id'] = df['race_id']

        print("特徴量:")
        for col in feature_columns:
            print(f"  - {col}")
        print()

        # 統計情報
        print("ターゲット（順位）分布:")
        print(df['rank'].value_counts().sort_index())
        print()

        return df[['group_id', 'race_id', 'horse_id', 'rank'] + feature_columns]

    finally:
        db.close()


def save_features(df, output_path):
    """特徴量を保存"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)
    print(f"✅ 特徴量を保存: {output_path}")
    print(f"   形状: {df.shape}")
    print()


if __name__ == "__main__":
    # 特徴量抽出
    df = extract_features_for_ranking()

    # 保存
    output_path = project_root / "analysis" / "output" / "learning_to_rank_features.csv"
    save_features(df, output_path)

    print("=" * 80)
    print("完了")
    print("=" * 80)
