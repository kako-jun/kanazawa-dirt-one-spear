#!/usr/bin/env python3
"""
ベンフォードの法則による公平性検証

ベンフォードの法則:
自然発生的な数値の最初の桁は、1が約30%、2が約18%...と特定の分布に従う。
もし人為的な操作や偏りがあると、この分布から外れる。

金沢競馬の結果（1着馬の馬番、配当など）がこの法則に従うかを検証し、
公平性を確認する。
"""

import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from scipy.stats import chisquare

# データベースパス
DB_PATH = Path(__file__).parent.parent / "backend" / "kanazawa_dirt_one_spear.db"

# ベンフォードの法則による期待分布
BENFORDS_DISTRIBUTION = {
    1: 0.301,
    2: 0.176,
    3: 0.125,
    4: 0.097,
    5: 0.079,
    6: 0.067,
    7: 0.058,
    8: 0.051,
    9: 0.046,
}


def get_connection():
    """データベース接続を取得"""
    return sqlite3.connect(DB_PATH)


def get_first_digit(number):
    """数値の最初の桁を取得"""
    if pd.isna(number) or number == 0:
        return None
    return int(str(abs(int(number)))[0])


def analyze_benfords_law(data, title="分析対象"):
    """ベンフォードの法則による検証"""
    # 最初の桁を抽出
    first_digits = [get_first_digit(x) for x in data if get_first_digit(x) is not None]

    if len(first_digits) == 0:
        print(f"\n{title}: データが不十分です")
        return

    # 観測分布を計算
    digit_counts = pd.Series(first_digits).value_counts().sort_index()
    total = len(first_digits)
    observed_dist = (digit_counts / total).to_dict()

    # 期待値を計算
    expected_counts = {digit: BENFORDS_DISTRIBUTION[digit] * total for digit in range(1, 10)}

    # データフレームにまとめる
    results = []
    for digit in range(1, 10):
        obs_count = digit_counts.get(digit, 0)
        obs_pct = observed_dist.get(digit, 0) * 100
        exp_pct = BENFORDS_DISTRIBUTION[digit] * 100
        exp_count = expected_counts[digit]

        results.append({
            "桁": digit,
            "観測数": obs_count,
            "観測%": round(obs_pct, 2),
            "期待%": round(exp_pct, 2),
            "差分": round(obs_pct - exp_pct, 2),
        })

    df = pd.DataFrame(results)

    # カイ二乗検定
    observed = [digit_counts.get(i, 0) for i in range(1, 10)]
    expected = [expected_counts[i] for i in range(1, 10)]
    chi2, p_value = chisquare(observed, expected)

    # 結果表示
    print("\n" + "=" * 80)
    print(f"{title} - ベンフォードの法則検証")
    print("=" * 80)
    print(f"\nサンプル数: {total:,}")
    print("\n【最初の桁の分布】")
    print(df.to_string(index=False))

    print(f"\n【統計検定結果】")
    print(f"カイ二乗値: {chi2:.4f}")
    print(f"p値: {p_value:.6f}")

    if p_value > 0.05:
        print("✅ ベンフォードの法則に従っている（公平性が示唆される）")
    elif p_value > 0.01:
        print("⚠️  ベンフォードの法則からやや逸脱（要注意）")
    else:
        print("❌ ベンフォードの法則から大きく逸脱（要調査）")

    return df, chi2, p_value


def analyze_winning_horse_numbers():
    """1着馬の馬番分析"""
    conn = get_connection()
    query = "SELECT first FROM results WHERE first IS NOT NULL"
    df = pd.read_sql_query(query, conn)
    conn.close()

    analyze_benfords_law(df["first"].values, "1着馬の馬番")


def analyze_trifecta_payouts():
    """3連単配当分析"""
    conn = get_connection()
    query = "SELECT payout_trifecta FROM results WHERE payout_trifecta IS NOT NULL"
    df = pd.read_sql_query(query, conn)
    conn.close()

    analyze_benfords_law(df["payout_trifecta"].values, "3連単配当")


def analyze_horse_weights():
    """馬体重分析"""
    conn = get_connection()
    query = "SELECT horse_weight FROM entries WHERE horse_weight IS NOT NULL"
    df = pd.read_sql_query(query, conn)
    conn.close()

    analyze_benfords_law(df["horse_weight"].values, "馬体重")


def analyze_race_distances():
    """レース距離分析（ベンフォードの法則には不適だが参考までに）"""
    conn = get_connection()
    query = "SELECT distance FROM races"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # 距離は固定値（1200m, 1400m等）が多いため、ベンフォードには不適
    # しかし参考として分析
    print("\n" + "=" * 80)
    print("レース距離の分布（参考）")
    print("=" * 80)
    print("※ レース距離は固定値が多いため、ベンフォードの法則には不適です")

    dist_counts = df["distance"].value_counts().sort_index()
    print("\n【距離別レース数】")
    for distance, count in dist_counts.items():
        pct = count / len(df) * 100
        print(f"{distance:4d}m: {count:4d}回 ({pct:5.2f}%)")


def main():
    """メイン実行関数"""
    print("金沢競馬データ - ベンフォードの法則による公平性検証")
    print(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"データベース: {DB_PATH}")

    print("\n" + "=" * 80)
    print("ベンフォードの法則とは")
    print("=" * 80)
    print("""
自然発生的な数値データの最初の桁は、以下の分布に従うという経験則:
  1: 30.1%
  2: 17.6%
  3: 12.5%
  4: 9.7%
  5: 7.9%
  6: 6.7%
  7: 5.8%
  8: 5.1%
  9: 4.6%

この法則は、会計不正の検出や選挙結果の公平性検証などに使われます。
金沢競馬の結果がこの法則に従えば、自然な結果（公平性）が示唆されます。
    """)

    # 各種データの検証
    analyze_winning_horse_numbers()
    analyze_trifecta_payouts()
    analyze_horse_weights()
    analyze_race_distances()

    print("\n" + "=" * 80)
    print("検証完了")
    print("=" * 80)
    print("""
【解釈のポイント】
- p値 > 0.05: ベンフォードの法則に従う → 公平性が示唆される
- p値 < 0.05: ベンフォードの法則から逸脱 → 何らかのパターンが存在
- 逸脱が必ずしも不正を意味するわけではありません
  - 競馬特有の構造（枠順の制約、馬番の割り当て方法など）による自然な偏り
  - サンプル数が少ない場合の統計的ゆらぎ

【次のステップ】
- 逸脱が見られた場合は、その原因を詳細に調査
- 年度別、距離別など、セグメント別の分析
- 他の公平性指標との組み合わせ
    """)


if __name__ == "__main__":
    main()
