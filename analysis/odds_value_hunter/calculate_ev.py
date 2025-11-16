#!/usr/bin/env python3
"""
期待値（Expected Value）計算スクリプト

EV = P(win) × Payout - Cost
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "backend"))

from app.database import SessionLocal, DB_PATH


def calculate_ev(win_probability, odds, bet_amount=100):
    """
    期待値を計算

    Args:
        win_probability: 勝率（0-1）
        odds: オッズ（倍率）
        bet_amount: 賭け金

    Returns:
        expected_value: 期待値
    """
    payout = bet_amount * odds
    ev = win_probability * payout - bet_amount
    return ev


def odds_to_implied_probability(odds):
    """
    オッズから暗黙の勝率を逆算

    Args:
        odds: オッズ（倍率）

    Returns:
        probability: 暗黙の勝率（0-1）
    """
    return 1 / odds if odds > 0 else 0


def calculate_bias_rate(ai_prob, odds_prob):
    """
    オッズバイアス率を計算

    Args:
        ai_prob: AI予測の勝率
        odds_prob: オッズ暗黙の勝率

    Returns:
        bias_rate: バイアス率（正なら過小評価）
    """
    if odds_prob == 0:
        return 0

    return (ai_prob - odds_prob) / odds_prob


def load_race_data_with_odds():
    """
    レースデータとオッズを読み込み
    """
    print("=" * 80)
    print("Odds Value Hunter: 期待値計算")
    print("=" * 80)
    print(f"DB: {DB_PATH}")
    print()

    db = SessionLocal()

    try:
        query = """
        SELECT
            r.id as race_id,
            r.race_date,
            r.track_condition,
            r.distance,

            rp.horse_id,
            rp.horse_number,
            rp.finish_position,
            rp.popularity,  -- 人気順位

            -- 馬の累積統計
            sh.win_rate as horse_win_rate,
            sh.place_rate as horse_place_rate

        FROM race_performances rp
        JOIN races r ON rp.race_id = r.id
        LEFT JOIN stat_horse_cumulative sh ON rp.horse_id = sh.horse_id
        WHERE rp.popularity IS NOT NULL
        ORDER BY r.race_date, rp.race_id, rp.popularity
        """

        df = pd.read_sql(query, db.connection())
        print(f"✅ データ取得完了: {len(df):,}件")
        print()

        return df

    finally:
        db.close()


def estimate_odds_from_popularity(popularity, num_horses=8):
    """
    人気順位からオッズを推定（簡易版）

    実際のオッズデータがない場合の暫定処理
    """
    # 簡易的なオッズマッピング
    odds_map = {
        1: 3.0,
        2: 5.0,
        3: 7.0,
        4: 10.0,
        5: 15.0,
        6: 20.0,
        7: 30.0,
        8: 50.0,
    }

    return odds_map.get(popularity, 50.0)


def analyze_value_bets(df):
    """
    期待値分析
    """
    df = df.copy()

    # オッズを推定（実際のオッズがない場合）
    df['estimated_odds'] = df['popularity'].apply(estimate_odds_from_popularity)

    # オッズから暗黙の勝率を計算
    df['odds_implied_prob'] = df['estimated_odds'].apply(odds_to_implied_probability)

    # AI予測の勝率（ここでは累積勝率を使用、本来はモデル予測）
    df['ai_win_prob'] = df['horse_win_rate'].fillna(0)

    # バイアス率を計算
    df['bias_rate'] = df.apply(
        lambda row: calculate_bias_rate(row['ai_win_prob'], row['odds_implied_prob']),
        axis=1
    )

    # 期待値を計算
    df['ev'] = df.apply(
        lambda row: calculate_ev(row['ai_win_prob'], row['estimated_odds']),
        axis=1
    )

    # バリューホースフラグ（期待値が正）
    df['is_value_bet'] = df['ev'] > 0

    return df


if __name__ == "__main__":
    # データ読み込み
    df = load_race_data_with_odds()

    # 期待値分析
    df = analyze_value_bets(df)

    # 結果表示
    print("=" * 80)
    print("期待値分析結果")
    print("=" * 80)

    print(f"総レコード数: {len(df):,}件")
    print(f"バリューベット: {df['is_value_bet'].sum():,}件 ({df['is_value_bet'].mean():.1%})")
    print()

    print("期待値統計:")
    print(df['ev'].describe())
    print()

    print("バイアス率統計:")
    print(df['bias_rate'].describe())
    print()

    # 保存
    output_path = project_root / "analysis" / "output" / "odds_value_analysis.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ 結果を保存: {output_path}")
    print()

    print("=" * 80)
    print("完了")
    print("=" * 80)
