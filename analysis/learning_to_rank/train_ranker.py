#!/usr/bin/env python3
"""
LightGBM Rankerの訓練スクリプト

LambdaRankを使って順位学習を行う。
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import GroupKFold

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "backend"))


def load_features(feature_path):
    """特徴量を読み込み"""
    df = pd.read_csv(feature_path)
    print(f"✅ 特徴量読み込み: {feature_path}")
    print(f"   形状: {df.shape}")
    print()
    return df


def prepare_lgb_dataset(df, feature_columns):
    """
    LightGBM Ranker用のDatasetを準備

    Args:
        df: DataFrame with group_id, rank, features
        feature_columns: list of feature column names

    Returns:
        lgb.Dataset
    """
    X = df[feature_columns].values
    y = df['rank'].values

    # group_idごとの馬の頭数を計算
    group_sizes = df.groupby('group_id').size().values

    print(f"特徴量: {len(feature_columns)}個")
    print(f"サンプル数: {len(X):,}件")
    print(f"グループ数: {len(group_sizes):,}件")
    print(f"平均グループサイズ: {group_sizes.mean():.1f}頭")
    print()

    dataset = lgb.Dataset(
        X,
        label=y,
        group=group_sizes,
    )

    return dataset


def train_ranker(train_data, valid_data=None):
    """
    LightGBM Rankerを訓練

    Args:
        train_data: lgb.Dataset for training
        valid_data: lgb.Dataset for validation (optional)

    Returns:
        trained model
    """
    params = {
        'objective': 'lambdarank',
        'metric': 'ndcg',
        'ndcg_eval_at': [1, 3, 5],  # 上位1, 3, 5頭の精度
        'learning_rate': 0.05,
        'num_leaves': 31,
        'max_depth': -1,
        'min_data_in_leaf': 20,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'verbose': 0,
    }

    print("パラメータ:")
    for key, value in params.items():
        print(f"  {key}: {value}")
    print()

    valid_sets = [train_data]
    valid_names = ['train']

    if valid_data is not None:
        valid_sets.append(valid_data)
        valid_names.append('valid')

    print("訓練開始...")
    model = lgb.train(
        params,
        train_data,
        num_boost_round=1000,
        valid_sets=valid_sets,
        valid_names=valid_names,
        callbacks=[
            lgb.early_stopping(stopping_rounds=50),
            lgb.log_evaluation(period=100),
        ],
    )

    print()
    print(f"✅ 訓練完了")
    print(f"   Best iteration: {model.best_iteration}")
    print(f"   Best score: {model.best_score}")
    print()

    return model


def save_model(model, output_path):
    """モデルを保存"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    model.save_model(str(output_path))
    print(f"✅ モデルを保存: {output_path}")
    print()


if __name__ == "__main__":
    print("=" * 80)
    print("Learning to Rank: LightGBM Ranker訓練")
    print("=" * 80)
    print()

    # 特徴量読み込み
    feature_path = project_root / "analysis" / "output" / "learning_to_rank_features.csv"
    df = load_features(feature_path)

    # 特徴量カラム
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

    # 時系列分割（最後の20%を検証用）
    split_idx = int(len(df) * 0.8)
    train_df = df.iloc[:split_idx]
    valid_df = df.iloc[split_idx:]

    print(f"訓練データ: {len(train_df):,}件 ({train_df['group_id'].nunique():,}レース)")
    print(f"検証データ: {len(valid_df):,}件 ({valid_df['group_id'].nunique():,}レース)")
    print()

    # Dataset準備
    train_data = prepare_lgb_dataset(train_df, feature_columns)
    valid_data = prepare_lgb_dataset(valid_df, feature_columns)

    # 訓練
    model = train_ranker(train_data, valid_data)

    # 保存
    model_path = project_root / "analysis" / "output" / "learning_to_rank_model.txt"
    save_model(model, model_path)

    print("=" * 80)
    print("完了")
    print("=" * 80)
