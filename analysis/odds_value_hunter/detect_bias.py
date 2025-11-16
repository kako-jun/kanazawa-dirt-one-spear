#!/usr/bin/env python3
"""
オッズバイアス検出スクリプト

過小評価されている馬（バリューホース）を発見する
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "backend"))


def load_analysis_results(csv_path):
    """期待値分析結果を読み込み"""
    df = pd.read_csv(csv_path)
    print(f"✅ 分析結果読み込み: {csv_path}")
    print(f"   形状: {df.shape}")
    print()
    return df


def detect_bias_patterns(df):
    """
    オッズバイアスのパターンを検出
    """
    print("=" * 80)
    print("オッズバイアスパターン分析")
    print("=" * 80)
    print()

    # 人気順位別のバイアス
    print("人気順位別のバイアス率:")
    bias_by_popularity = df.groupby('popularity').agg({
        'bias_rate': ['mean', 'std', 'count'],
        'is_value_bet': 'mean',
    })
    print(bias_by_popularity)
    print()

    # 過小評価されやすい人気帯を特定
    print("バリューベット率が高い人気帯:")
    value_rate = df.groupby('popularity')['is_value_bet'].mean().sort_values(ascending=False)
    print(value_rate.head(5))
    print()

    return bias_by_popularity


def find_value_horses(df, threshold=0.1):
    """
    バリューホースを抽出

    Args:
        df: DataFrame
        threshold: 期待値の閾値

    Returns:
        DataFrame of value horses
    """
    value_horses = df[df['ev'] > threshold].copy()
    value_horses = value_horses.sort_values('ev', ascending=False)

    print(f"期待値 > {threshold}の馬: {len(value_horses):,}件")

    if len(value_horses) > 0:
        print()
        print("トップ10のバリューベット:")
        print(value_horses.head(10)[['race_date', 'horse_id', 'popularity', 'ai_win_prob', 'odds_implied_prob', 'bias_rate', 'ev', 'finish_position']])
        print()

    return value_horses


def visualize_bias(df, output_dir):
    """バイアスを可視化"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. AI予測 vs オッズ暗黙確率の散布図
    plt.figure(figsize=(10, 8))
    plt.scatter(df['odds_implied_prob'], df['ai_win_prob'], alpha=0.3, s=10)
    plt.plot([0, 0.5], [0, 0.5], 'r--', label='Perfect Calibration')
    plt.xlabel('Odds Implied Probability')
    plt.ylabel('AI Win Probability')
    plt.title('AI Prediction vs Odds Implied Probability')
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / 'ai_vs_odds_scatter.png')
    print(f"✅ 散布図を保存: {output_dir / 'ai_vs_odds_scatter.png'}")

    # 2. 人気順位別のバイアス率
    plt.figure(figsize=(10, 6))
    bias_by_pop = df.groupby('popularity')['bias_rate'].mean()
    plt.bar(bias_by_pop.index, bias_by_pop.values)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.xlabel('Popularity')
    plt.ylabel('Average Bias Rate')
    plt.title('Bias Rate by Popularity')
    plt.tight_layout()
    plt.savefig(output_dir / 'bias_by_popularity.png')
    print(f"✅ 人気別バイアス図を保存: {output_dir / 'bias_by_popularity.png'}")

    plt.close('all')


if __name__ == "__main__":
    print("=" * 80)
    print("Odds Value Hunter: バイアス検出")
    print("=" * 80)
    print()

    # 分析結果読み込み
    csv_path = project_root / "analysis" / "output" / "odds_value_analysis.csv"
    df = load_analysis_results(csv_path)

    # バイアスパターン分析
    bias_patterns = detect_bias_patterns(df)

    # バリューホース抽出
    value_horses = find_value_horses(df, threshold=10)

    # 可視化
    output_dir = project_root / "analysis" / "output" / "odds_bias_plots"
    visualize_bias(df, output_dir)

    print()
    print("=" * 80)
    print("完了")
    print("=" * 80)
