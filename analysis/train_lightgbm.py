#!/usr/bin/env python3
"""
LightGBM予想モデルの訓練

オッズあり/なしの2つのモデルを訓練し、評価する
"""

import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    log_loss
)
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from datetime import datetime

# プロジェクトルート
project_root = Path(__file__).parent.parent


def detect_gpu():
    """
    GPU利用可能かどうかを検出

    Returns:
        bool: GPU利用可能ならTrue
    """
    try:
        # LightGBM GPU版がインストールされているかチェック
        import lightgbm as lgb

        # 簡易的なGPU検出: NVIDIAのGPUをチェック
        try:
            import subprocess
            result = subprocess.run(['nvidia-smi'],
                                  capture_output=True,
                                  text=True,
                                  timeout=5)
            if result.returncode == 0:
                print("GPU detected (NVIDIA)")
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        print("GPU not detected, using CPU")
        return False

    except Exception as e:
        print(f"Error detecting GPU: {e}")
        return False

# 出力ディレクトリ
OUTPUT_DIR = project_root / "analysis" / "output" / "models"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FEATURES_PATH = project_root / "analysis" / "output" / "features" / "features.csv"


def load_features():
    """特徴量データを読み込む"""
    print("Loading features...")
    df = pd.read_csv(FEATURES_PATH)
    df['race_date'] = pd.to_datetime(df['race_date'])
    print(f"Loaded {len(df)} samples, {len(df.columns)} columns")
    return df


def prepare_dataset(df, include_popularity=False):
    """
    データセットを準備

    Args:
        df: 特徴量データフレーム
        include_popularity: 人気（オッズ情報）を特徴量に含めるか

    Returns:
        X, y, feature_names
    """
    print(f"Preparing dataset (include_popularity={include_popularity})...")

    # 除外するカラム（IDや目的変数など）
    exclude_cols = [
        'performance_id',
        'race_id',
        'horse_id',
        'jockey_id',
        'trainer_id',
        'race_date',
        'track_condition',
        'distance_category',
        'finish_position',
        'target_win',
        'target_place'
    ]

    # popularityの扱い
    if not include_popularity:
        exclude_cols.append('popularity')

    # 特徴量カラムを選択
    feature_cols = [col for col in df.columns if col not in exclude_cols]

    X = df[feature_cols].copy()
    y = df['target_win'].copy()  # 1着予想

    # 欠損値処理
    X = X.fillna(0)

    print(f"Features: {len(feature_cols)}")
    print(f"Feature list: {feature_cols}")
    print(f"Target distribution: {y.value_counts().to_dict()}")

    return X, y, feature_cols


def time_series_split_by_date(df, n_splits=5):
    """
    日付ベースの時系列分割

    Args:
        df: データフレーム（race_dateカラムを含む）
        n_splits: 分割数

    Returns:
        train/validのインデックスのリスト
    """
    df = df.sort_values('race_date').reset_index(drop=True)
    unique_dates = df['race_date'].unique()
    unique_dates.sort()

    n_dates = len(unique_dates)
    split_size = n_dates // (n_splits + 1)

    splits = []
    for i in range(n_splits):
        # 訓練データ: 開始から (i+1)*split_size まで
        # 検証データ: (i+1)*split_size から (i+2)*split_size まで
        train_end_date = unique_dates[(i + 1) * split_size]
        valid_end_date = unique_dates[min((i + 2) * split_size, n_dates - 1)]

        train_idx = df[df['race_date'] <= train_end_date].index.tolist()
        valid_idx = df[(df['race_date'] > train_end_date) & (df['race_date'] <= valid_end_date)].index.tolist()

        splits.append((train_idx, valid_idx))

    return splits


def train_model(X_train, y_train, X_valid, y_valid, params=None, use_gpu=False):
    """
    LightGBMモデルを訓練

    Args:
        X_train, y_train: 訓練データ
        X_valid, y_valid: 検証データ
        params: LightGBMのパラメータ
        use_gpu: GPUを使用するか

    Returns:
        trained model
    """
    if params is None:
        params = {
            'objective': 'binary',
            'metric': 'binary_logloss',
            'boosting_type': 'gbdt',
            'num_leaves': 31,
            'learning_rate': 0.05,
            'feature_fraction': 0.8,
            'bagging_fraction': 0.8,
            'bagging_freq': 5,
            'verbose': -1,
            'seed': 42
        }

    # GPU設定
    if use_gpu:
        params['device'] = 'gpu'
        params['gpu_platform_id'] = 0
        params['gpu_device_id'] = 0
        print("Training with GPU acceleration")

    train_data = lgb.Dataset(X_train, label=y_train)
    valid_data = lgb.Dataset(X_valid, label=y_valid, reference=train_data)

    model = lgb.train(
        params,
        train_data,
        num_boost_round=1000,
        valid_sets=[train_data, valid_data],
        valid_names=['train', 'valid'],
        callbacks=[
            lgb.early_stopping(stopping_rounds=50, verbose=False),
            lgb.log_evaluation(period=100)
        ]
    )

    return model


def evaluate_model(model, X, y, dataset_name="Test"):
    """
    モデルを評価

    Args:
        model: 訓練済みモデル
        X: 特徴量
        y: 正解ラベル
        dataset_name: データセット名

    Returns:
        評価指標の辞書
    """
    y_pred_proba = model.predict(X, num_iteration=model.best_iteration)
    y_pred = (y_pred_proba >= 0.5).astype(int)

    metrics = {
        'accuracy': accuracy_score(y, y_pred),
        'precision': precision_score(y, y_pred, zero_division=0),
        'recall': recall_score(y, y_pred, zero_division=0),
        'f1': f1_score(y, y_pred, zero_division=0),
        'roc_auc': roc_auc_score(y, y_pred_proba),
        'logloss': log_loss(y, y_pred_proba)
    }

    print(f"\n{dataset_name} Metrics:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.4f}")

    return metrics


def plot_feature_importance(model, feature_names, output_path):
    """特徴量重要度をプロット"""
    importance = model.feature_importance(importance_type='gain')
    feature_importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importance
    }).sort_values('importance', ascending=False)

    # Top 20を表示
    plt.figure(figsize=(10, 8))
    top_features = feature_importance_df.head(20)
    sns.barplot(data=top_features, x='importance', y='feature')
    plt.title('Feature Importance (Top 20)')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    # CSV保存
    csv_path = output_path.with_suffix('.csv')
    feature_importance_df.to_csv(csv_path, index=False)

    print(f"Feature importance saved: {output_path}")


def save_model(model, model_path):
    """モデルを保存"""
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model saved: {model_path}")


def main():
    """メイン処理"""
    print("=== LightGBM Training ===\n")

    # GPU検出
    use_gpu = detect_gpu()
    print()

    # 特徴量読み込み
    df = load_features()

    # 時系列分割（5-fold）
    print("\nCreating time series splits...")
    splits = time_series_split_by_date(df, n_splits=5)
    print(f"Created {len(splits)} splits")

    # === モデル1: オッズなし（popularity除外） ===
    print("\n" + "="*60)
    print("Training Model WITHOUT Popularity (Odds)")
    print("="*60)

    X_no_odds, y, feature_names_no_odds = prepare_dataset(df, include_popularity=False)

    cv_metrics_no_odds = []
    for fold, (train_idx, valid_idx) in enumerate(splits, 1):
        print(f"\n--- Fold {fold}/{len(splits)} ---")
        X_train, X_valid = X_no_odds.iloc[train_idx], X_no_odds.iloc[valid_idx]
        y_train, y_valid = y.iloc[train_idx], y.iloc[valid_idx]

        model = train_model(X_train, y_train, X_valid, y_valid, use_gpu=use_gpu)
        metrics = evaluate_model(model, X_valid, y_valid, f"Valid Fold {fold}")
        cv_metrics_no_odds.append(metrics)

        # 最後のfoldのモデルを保存
        if fold == len(splits):
            model_path = OUTPUT_DIR / "lightgbm_no_odds.pkl"
            save_model(model, model_path)

            importance_path = OUTPUT_DIR / "feature_importance_no_odds.png"
            plot_feature_importance(model, feature_names_no_odds, importance_path)

    # CV平均
    print("\n--- CV Average (No Odds) ---")
    for metric in cv_metrics_no_odds[0].keys():
        avg_value = np.mean([m[metric] for m in cv_metrics_no_odds])
        std_value = np.std([m[metric] for m in cv_metrics_no_odds])
        print(f"  {metric}: {avg_value:.4f} ± {std_value:.4f}")

    # === モデル2: オッズあり（popularity含む） ===
    print("\n" + "="*60)
    print("Training Model WITH Popularity (Odds)")
    print("="*60)

    X_with_odds, y, feature_names_with_odds = prepare_dataset(df, include_popularity=True)

    cv_metrics_with_odds = []
    for fold, (train_idx, valid_idx) in enumerate(splits, 1):
        print(f"\n--- Fold {fold}/{len(splits)} ---")
        X_train, X_valid = X_with_odds.iloc[train_idx], X_with_odds.iloc[valid_idx]
        y_train, y_valid = y.iloc[train_idx], y.iloc[valid_idx]

        model = train_model(X_train, y_train, X_valid, y_valid, use_gpu=use_gpu)
        metrics = evaluate_model(model, X_valid, y_valid, f"Valid Fold {fold}")
        cv_metrics_with_odds.append(metrics)

        # 最後のfoldのモデルを保存
        if fold == len(splits):
            model_path = OUTPUT_DIR / "lightgbm_with_odds.pkl"
            save_model(model, model_path)

            importance_path = OUTPUT_DIR / "feature_importance_with_odds.png"
            plot_feature_importance(model, feature_names_with_odds, importance_path)

    # CV平均
    print("\n--- CV Average (With Odds) ---")
    for metric in cv_metrics_with_odds[0].keys():
        avg_value = np.mean([m[metric] for m in cv_metrics_with_odds])
        std_value = np.std([m[metric] for m in cv_metrics_with_odds])
        print(f"  {metric}: {avg_value:.4f} ± {std_value:.4f}")

    # === 比較結果を保存 ===
    comparison_df = pd.DataFrame({
        'metric': list(cv_metrics_no_odds[0].keys()),
        'no_odds_mean': [np.mean([m[k] for m in cv_metrics_no_odds]) for k in cv_metrics_no_odds[0].keys()],
        'no_odds_std': [np.std([m[k] for m in cv_metrics_no_odds]) for k in cv_metrics_no_odds[0].keys()],
        'with_odds_mean': [np.mean([m[k] for m in cv_metrics_with_odds]) for k in cv_metrics_with_odds[0].keys()],
        'with_odds_std': [np.std([m[k] for m in cv_metrics_with_odds]) for k in cv_metrics_with_odds[0].keys()]
    })

    comparison_path = OUTPUT_DIR / "model_comparison.csv"
    comparison_df.to_csv(comparison_path, index=False)
    print(f"\nComparison saved: {comparison_path}")

    print("\n=== Training Complete ===")


if __name__ == "__main__":
    main()
