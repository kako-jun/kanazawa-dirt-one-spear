#!/usr/bin/env python3
"""
Learning to Rank モデルの評価
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.metrics import ndcg_score

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "backend"))


def load_model(model_path):
    """モデル読み込み"""
    model = lgb.Booster(model_file=str(model_path))
    print(f"✅ モデル読み込み: {model_path}")
    return model


def predict_ranks(model, df, feature_columns):
    """
    順位を予測

    Returns:
        DataFrame with predicted_rank column
    """
    X = df[feature_columns].values
    scores = model.predict(X)

    # レースごとにスコアでソートして順位を割り当て
    df = df.copy()
    df['predicted_score'] = scores
    df['predicted_rank'] = df.groupby('group_id')['predicted_score'].rank(ascending=False, method='first')

    return df


def evaluate_ndcg(df):
    """NDCG@kを計算"""
    ndcg_at = [1, 3, 5]
    results = {}

    for k in ndcg_at:
        # レースごとにNDCGを計算
        ndcg_scores = []
        for race_id, group in df.groupby('group_id'):
            y_true = group['rank'].values
            y_pred = group['predicted_score'].values

            if len(y_true) >= k:
                ndcg = ndcg_score([y_true], [y_pred], k=k)
                ndcg_scores.append(ndcg)

        results[f'NDCG@{k}'] = np.mean(ndcg_scores)

    return results


def evaluate_hit_rate(df):
    """3連単的中率を計算"""
    correct = 0
    total = 0

    for race_id, group in df.groupby('group_id'):
        # 実際の1-2-3着
        actual_top3 = group.nsmallest(3, 'rank')['horse_id'].tolist()

        # 予測の1-2-3着
        predicted_top3 = group.nsmallest(3, 'predicted_rank')['horse_id'].tolist()

        # 完全一致チェック
        if actual_top3 == predicted_top3:
            correct += 1

        total += 1

    hit_rate = correct / total if total > 0 else 0
    return hit_rate, correct, total


if __name__ == "__main__":
    print("=" * 80)
    print("Learning to Rank: モデル評価")
    print("=" * 80)
    print()

    # データ読み込み
    feature_path = project_root / "analysis" / "output" / "learning_to_rank_features.csv"
    df = pd.read_csv(feature_path)

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

    # 検証データ（最後の20%）
    split_idx = int(len(df) * 0.8)
    test_df = df.iloc[split_idx:]

    print(f"テストデータ: {len(test_df):,}件 ({test_df['group_id'].nunique():,}レース)")
    print()

    # モデル読み込み
    model_path = project_root / "analysis" / "output" / "learning_to_rank_model.txt"
    model = load_model(model_path)
    print()

    # 予測
    print("予測中...")
    test_df = predict_ranks(model, test_df, feature_columns)
    print("✅ 予測完了")
    print()

    # 評価
    print("=" * 80)
    print("評価結果")
    print("=" * 80)

    # NDCG
    ndcg_results = evaluate_ndcg(test_df)
    for metric, score in ndcg_results.items():
        print(f"{metric}: {score:.4f}")

    print()

    # 3連単的中率
    hit_rate, correct, total = evaluate_hit_rate(test_df)
    print(f"3連単的中率: {hit_rate:.2%} ({correct}/{total})")
    print(f"ベースライン: {1/336:.2%} (ランダム)")
    print()

    print("=" * 80)
    print("完了")
    print("=" * 80)
