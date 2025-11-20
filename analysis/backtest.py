#!/usr/bin/env python3
"""
作戦１「王道」のバックテスト

訓練済みモデルを使って過去レースの予想をシミュレートし、
実際の的中率・回収率を検証する。
"""

import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
import pickle
from datetime import datetime
import sqlite3

# プロジェクトルート
project_root = Path(__file__).parent.parent

# パス設定
DB_PATH = project_root / "backend" / "data" / "kanazawa_dirt_one_spear.db"
MODEL_NO_ODDS = project_root / "analysis" / "output" / "models" / "lightgbm_no_odds.pkl"
MODEL_WITH_ODDS = project_root / "analysis" / "output" / "models" / "lightgbm_with_odds.pkl"
OUTPUT_DIR = project_root / "analysis" / "output" / "backtest"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def get_connection():
    """DB接続を取得"""
    return sqlite3.connect(DB_PATH)


def load_model(model_path):
    """訓練済みモデルを読み込む"""
    print(f"Loading model: {model_path}")
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model


def load_test_data(train_cutoff_date='2024-01-01'):
    """
    テストデータを読み込む

    Args:
        train_cutoff_date: この日付以降をテストデータとする

    Returns:
        DataFrame
    """
    conn = get_connection()

    # 特徴量生成と同じクエリ（test期間のみ）
    query = f"""
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

        -- 馬の累積統計
        hc.total_races as horse_total_races,
        COALESCE(hc.win_rate, 0.0) as horse_win_rate,
        COALESCE(hc.place_rate, 0.0) as horse_place_rate,
        COALESCE(hc.avg_finish_position, 8.0) as horse_avg_finish,
        COALESCE(hc.days_since_last_race, 999) as horse_days_since_last_race,

        -- 騎手の累積統計
        jc.total_races as jockey_total_races,
        COALESCE(jc.win_rate, 0.0) as jockey_win_rate,
        COALESCE(jc.place_rate, 0.0) as jockey_place_rate,
        COALESCE(jc.avg_finish_position, 5.0) as jockey_avg_finish,

        -- 調教師の累積統計
        tc.total_races as trainer_total_races,
        COALESCE(tc.win_rate, 0.0) as trainer_win_rate,
        COALESCE(tc.place_rate, 0.0) as trainer_place_rate

    FROM race_performances rp
    JOIN races r ON rp.race_id = r.race_id
    JOIN entries e ON rp.entry_id = e.entry_id

    -- 統計テーブルをJOIN
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
      AND r.date >= '{train_cutoff_date}'
    ORDER BY r.date, r.race_id, rp.horse_number
    """

    print(f"Loading test data (from {train_cutoff_date})...")
    df = pd.read_sql_query(query, conn)
    df['race_date'] = pd.to_datetime(df['race_date'])
    conn.close()

    print(f"Loaded {len(df)} performances, {df['race_id'].nunique()} races")
    return df


def add_race_features(df):
    """レース条件の特徴量を追加"""
    # 馬場状態ワンホット
    track_dummies = pd.get_dummies(df['track_condition'], prefix='track')

    # 距離カテゴリ
    df['distance_category'] = pd.cut(
        df['distance'],
        bins=[0, 1400, 1600, 1800, 2000, 10000],
        labels=['1300-1400m', '1500-1600m', '1700-1800m', '1900-2000m', '2100m-']
    )
    distance_dummies = pd.get_dummies(df['distance_category'], prefix='distance')

    return pd.concat([df, track_dummies, distance_dummies], axis=1)


def prepare_features(df, include_popularity):
    """特徴量を準備（訓練時と同じ処理）"""
    exclude_cols = [
        'performance_id', 'race_id', 'horse_id', 'jockey_id', 'trainer_id',
        'race_date', 'track_condition', 'distance_category',
        'finish_position'
    ]

    if not include_popularity:
        exclude_cols.append('popularity')

    feature_cols = [col for col in df.columns if col not in exclude_cols]
    X = df[feature_cols].copy().fillna(0)

    return X, feature_cols


def predict_race(race_df, model, include_popularity):
    """
    1レースの予想を行う

    Args:
        race_df: レース内の全馬のデータ
        model: 訓練済みモデル
        include_popularity: 人気情報を使うか

    Returns:
        予想結果（horse_number, win_prob, predicted_rank）
    """
    X, _ = prepare_features(race_df, include_popularity)

    # 1着確率を予測
    win_probs = model.predict(X, num_iteration=model.best_iteration)

    # 確率順にランク付け
    race_df = race_df.copy()
    race_df['win_prob'] = win_probs
    race_df = race_df.sort_values('win_prob', ascending=False).reset_index(drop=True)
    race_df['predicted_rank'] = range(1, len(race_df) + 1)

    return race_df[['horse_number', 'finish_position', 'win_prob', 'predicted_rank']]


def construct_trifecta(prediction_df):
    """
    3連単を構築

    上位3頭から1-2-3の組み合わせを作成

    Args:
        prediction_df: 予想結果（predicted_rankでソート済み）

    Returns:
        (1着馬番, 2着馬番, 3着馬番)
    """
    if len(prediction_df) < 3:
        return None

    top3 = prediction_df.nsmallest(3, 'predicted_rank')
    return tuple(top3['horse_number'].tolist())


def get_actual_trifecta(race_df):
    """
    実際の3連単結果を取得

    Args:
        race_df: レース内の全馬のデータ

    Returns:
        (1着馬番, 2着馬番, 3着馬番) or None
    """
    top3 = race_df.nsmallest(3, 'finish_position')
    if len(top3) < 3:
        return None
    return tuple(top3['horse_number'].tolist())


def get_trifecta_payout(race_id):
    """
    3連単の配当を取得

    Args:
        race_id: レースID

    Returns:
        配当額（円）, None if not found
    """
    conn = get_connection()
    query = f"""
    SELECT payout
    FROM payouts
    WHERE race_id = '{race_id}'
      AND payout_type = 'trifecta'
    LIMIT 1
    """
    result = pd.read_sql_query(query, conn)
    conn.close()

    if len(result) > 0:
        return result['payout'].iloc[0]
    return None


def run_backtest(model, model_name, test_df, include_popularity):
    """
    バックテスト実行

    Args:
        model: 訓練済みモデル
        model_name: モデル名（レポート用）
        test_df: テストデータ
        include_popularity: 人気情報を使うか

    Returns:
        結果のDataFrame
    """
    print(f"\n{'='*60}")
    print(f"Running Backtest: {model_name}")
    print(f"{'='*60}\n")

    results = []
    race_ids = test_df['race_id'].unique()

    for i, race_id in enumerate(race_ids, 1):
        race_df = test_df[test_df['race_id'] == race_id].copy()
        race_date = race_df['race_date'].iloc[0]

        # 予想実行
        prediction = predict_race(race_df, model, include_popularity)
        predicted_trifecta = construct_trifecta(prediction)
        actual_trifecta = get_actual_trifecta(race_df)

        if predicted_trifecta is None or actual_trifecta is None:
            continue

        # 的中判定
        is_hit = (predicted_trifecta == actual_trifecta)

        # 配当取得
        payout = get_trifecta_payout(race_id) if is_hit else 0

        results.append({
            'race_id': race_id,
            'race_date': race_date,
            'predicted': predicted_trifecta,
            'actual': actual_trifecta,
            'is_hit': is_hit,
            'payout': payout,
            'investment': 100  # 1点100円
        })

        if i % 100 == 0:
            print(f"Processed {i}/{len(race_ids)} races...")

    results_df = pd.DataFrame(results)
    return results_df


def calculate_metrics(results_df):
    """
    バックテスト結果から指標を計算

    Returns:
        指標の辞書
    """
    total_races = len(results_df)
    total_hits = results_df['is_hit'].sum()
    hit_rate = total_hits / total_races if total_races > 0 else 0

    total_investment = results_df['investment'].sum()
    total_return = results_df['payout'].sum()
    roi = (total_return / total_investment) if total_investment > 0 else 0

    avg_payout = results_df[results_df['is_hit']]['payout'].mean() if total_hits > 0 else 0

    metrics = {
        'total_races': total_races,
        'total_hits': total_hits,
        'hit_rate': hit_rate,
        'total_investment': total_investment,
        'total_return': total_return,
        'roi': roi,
        'profit': total_return - total_investment,
        'avg_payout': avg_payout
    }

    return metrics


def print_metrics(metrics, model_name):
    """指標を表示"""
    print(f"\n{'='*60}")
    print(f"{model_name} - Backtest Results")
    print(f"{'='*60}\n")

    print(f"Total Races:       {metrics['total_races']:>10,}")
    print(f"Hits:              {metrics['total_hits']:>10,}")
    print(f"Hit Rate:          {metrics['hit_rate']:>10.2%}")
    print(f"\nTotal Investment:  {metrics['total_investment']:>10,} 円")
    print(f"Total Return:      {metrics['total_return']:>10,} 円")
    print(f"Profit/Loss:       {metrics['profit']:>10,} 円")
    print(f"ROI:               {metrics['roi']:>10.2%}")
    print(f"\nAvg Payout (hit):  {metrics['avg_payout']:>10,.0f} 円")


def save_results(results_df, metrics, model_name, output_dir):
    """結果を保存"""
    timestamp = datetime.now().strftime("%Y%m%d")

    # 詳細結果CSV
    results_path = output_dir / f"backtest_{model_name}_{timestamp}.csv"
    results_df.to_csv(results_path, index=False)
    print(f"\nResults saved: {results_path}")

    # サマリーレポート
    report_path = output_dir / f"backtest_summary_{model_name}_{timestamp}.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"{'='*60}\n")
        f.write(f"{model_name} - Backtest Summary\n")
        f.write(f"{'='*60}\n\n")
        f.write(f"Total Races:       {metrics['total_races']:>10,}\n")
        f.write(f"Hits:              {metrics['total_hits']:>10,}\n")
        f.write(f"Hit Rate:          {metrics['hit_rate']:>10.2%}\n")
        f.write(f"\nTotal Investment:  {metrics['total_investment']:>10,} 円\n")
        f.write(f"Total Return:      {metrics['total_return']:>10,} 円\n")
        f.write(f"Profit/Loss:       {metrics['profit']:>10,} 円\n")
        f.write(f"ROI:               {metrics['roi']:>10.2%}\n")
        f.write(f"\nAvg Payout (hit):  {metrics['avg_payout']:>10,.0f} 円\n")

    print(f"Summary saved: {report_path}")


def main():
    """メイン処理"""
    print("=== 作戦１「王道」バックテスト ===\n")

    # テストデータ読み込み
    test_df = load_test_data(train_cutoff_date='2024-01-01')
    test_df = add_race_features(test_df)

    print(f"\nTest period: {test_df['race_date'].min()} to {test_df['race_date'].max()}")
    print(f"Total races: {test_df['race_id'].nunique()}")

    # モデル1: オッズなし
    print("\n" + "="*60)
    print("Model 1: No Odds")
    print("="*60)
    model_no_odds = load_model(MODEL_NO_ODDS)
    results_no_odds = run_backtest(
        model_no_odds,
        "No Odds Model",
        test_df,
        include_popularity=False
    )
    metrics_no_odds = calculate_metrics(results_no_odds)
    print_metrics(metrics_no_odds, "No Odds Model")
    save_results(results_no_odds, metrics_no_odds, "no_odds", OUTPUT_DIR)

    # モデル2: オッズあり
    print("\n" + "="*60)
    print("Model 2: With Odds")
    print("="*60)
    model_with_odds = load_model(MODEL_WITH_ODDS)
    results_with_odds = run_backtest(
        model_with_odds,
        "With Odds Model",
        test_df,
        include_popularity=True
    )
    metrics_with_odds = calculate_metrics(results_with_odds)
    print_metrics(metrics_with_odds, "With Odds Model")
    save_results(results_with_odds, metrics_with_odds, "with_odds", OUTPUT_DIR)

    # 比較レポート
    print("\n" + "="*60)
    print("Model Comparison")
    print("="*60)
    print(f"\n{'Metric':<25} {'No Odds':>15} {'With Odds':>15}")
    print("-" * 60)
    print(f"{'Hit Rate':<25} {metrics_no_odds['hit_rate']:>14.2%} {metrics_with_odds['hit_rate']:>14.2%}")
    print(f"{'ROI':<25} {metrics_no_odds['roi']:>14.2%} {metrics_with_odds['roi']:>14.2%}")
    print(f"{'Profit/Loss':<25} {metrics_no_odds['profit']:>14,} {metrics_with_odds['profit']:>14,}")

    print("\n=== Backtest Complete ===")


if __name__ == "__main__":
    main()
