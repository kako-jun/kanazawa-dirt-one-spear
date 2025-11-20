#!/usr/bin/env python3
"""
予想と人気の相関分析

バックテスト結果を分析し、以下を確認：
1. 予想上位馬の平均人気
2. 人気薄を選べているか
3. ボックス買いのシミュレーション
"""

import pandas as pd
import numpy as np
from pathlib import Path

project_root = Path(__file__).parent.parent
BACKTEST_DIR = project_root / "analysis" / "output" / "backtest"


def load_results(model_name):
    """バックテスト結果を読み込む"""
    csv_path = BACKTEST_DIR / f"backtest_{model_name}_20251120.csv"
    return pd.read_csv(csv_path)


def analyze_popularity_correlation():
    """人気と予想の相関を分析"""
    import sqlite3
    from pathlib import Path

    DB_PATH = project_root / "backend" / "data" / "kanazawa_dirt_one_spear.db"
    conn = sqlite3.connect(DB_PATH)

    # 2024年以降のデータで人気順位を取得
    query = """
    SELECT
        rp.race_id,
        rp.horse_number,
        rp.popularity,
        rp.finish_position
    FROM race_performances rp
    JOIN races r ON rp.race_id = r.race_id
    WHERE r.date >= '2024-01-01'
      AND rp.popularity IS NOT NULL
    ORDER BY r.date, rp.race_id, rp.horse_number
    """

    popularity_df = pd.read_sql_query(query, conn)
    conn.close()

    return popularity_df


def main():
    print("=== 予想と人気の相関分析 ===\n")

    # バックテスト結果読み込み
    results_with_odds = load_results("with_odds")
    popularity_df = analyze_popularity_correlation()

    # 予想馬番を展開
    results_with_odds['predicted_1st'] = results_with_odds['predicted'].apply(
        lambda x: eval(x)[0] if isinstance(x, str) else x[0]
    )
    results_with_odds['predicted_2nd'] = results_with_odds['predicted'].apply(
        lambda x: eval(x)[1] if isinstance(x, str) else x[1]
    )
    results_with_odds['predicted_3rd'] = results_with_odds['predicted'].apply(
        lambda x: eval(x)[2] if isinstance(x, str) else x[2]
    )

    # 実際の馬番を展開
    results_with_odds['actual_1st'] = results_with_odds['actual'].apply(
        lambda x: eval(x)[0] if isinstance(x, str) else x[0]
    )
    results_with_odds['actual_2nd'] = results_with_odds['actual'].apply(
        lambda x: eval(x)[1] if isinstance(x, str) else x[1]
    )
    results_with_odds['actual_3rd'] = results_with_odds['actual'].apply(
        lambda x: eval(x)[2] if isinstance(x, str) else x[2]
    )

    # 人気データとマージ
    merged = []
    for _, row in results_with_odds.iterrows():
        race_id = row['race_id']
        race_pop = popularity_df[popularity_df['race_id'] == race_id]

        if len(race_pop) == 0:
            continue

        # 予想馬の人気
        pred_1st_pop = race_pop[race_pop['horse_number'] == row['predicted_1st']]['popularity'].values
        pred_2nd_pop = race_pop[race_pop['horse_number'] == row['predicted_2nd']]['popularity'].values
        pred_3rd_pop = race_pop[race_pop['horse_number'] == row['predicted_3rd']]['popularity'].values

        merged.append({
            'race_id': race_id,
            'predicted_1st': row['predicted_1st'],
            'predicted_2nd': row['predicted_2nd'],
            'predicted_3rd': row['predicted_3rd'],
            'pred_1st_pop': pred_1st_pop[0] if len(pred_1st_pop) > 0 else None,
            'pred_2nd_pop': pred_2nd_pop[0] if len(pred_2nd_pop) > 0 else None,
            'pred_3rd_pop': pred_3rd_pop[0] if len(pred_3rd_pop) > 0 else None,
            'is_hit': row['is_hit'],
            'payout': row['payout']
        })

    analysis_df = pd.DataFrame(merged)

    # 分析1: 予想馬の平均人気
    print("【分析1】予想馬の平均人気順位")
    print("-" * 50)
    print(f"1着予想の平均人気: {analysis_df['pred_1st_pop'].mean():.2f}位")
    print(f"2着予想の平均人気: {analysis_df['pred_2nd_pop'].mean():.2f}位")
    print(f"3着予想の平均人気: {analysis_df['pred_3rd_pop'].mean():.2f}位")
    print(f"\n予想上位3頭の平均人気: {analysis_df[['pred_1st_pop', 'pred_2nd_pop', 'pred_3rd_pop']].mean().mean():.2f}位")

    # 分析2: 1番人気を選ぶ確率
    print(f"\n【分析2】1番人気を1着予想に選ぶ確率")
    print("-" * 50)
    pop1_rate = (analysis_df['pred_1st_pop'] == 1).mean()
    print(f"1着予想が1番人気: {pop1_rate:.2%}")

    # 分析3: 人気上位3頭の予想率
    print(f"\n【分析3】予想馬が人気上位3頭以内の確率")
    print("-" * 50)
    top3_1st = (analysis_df['pred_1st_pop'] <= 3).mean()
    top3_2nd = (analysis_df['pred_2nd_pop'] <= 3).mean()
    top3_3rd = (analysis_df['pred_3rd_pop'] <= 3).mean()
    print(f"1着予想が人気3位以内: {top3_1st:.2%}")
    print(f"2着予想が人気3位以内: {top3_2nd:.2%}")
    print(f"3着予想が人気3位以内: {top3_3rd:.2%}")

    # 分析4: ボックス買いシミュレーション
    print(f"\n【分析4】ボックス買いシミュレーション（上位3頭）")
    print("-" * 50)

    box_hits = 0
    box_return = 0
    box_investment = len(results_with_odds) * 6 * 100  # 6点×100円

    for _, row in results_with_odds.iterrows():
        pred_set = {row['predicted_1st'], row['predicted_2nd'], row['predicted_3rd']}
        actual_set = {row['actual_1st'], row['actual_2nd'], row['actual_3rd']}

        # 3頭全てが含まれているか
        if pred_set == actual_set:
            box_hits += 1
            # 配当は3連単の1/6（簡易計算）
            box_return += row['payout']

    box_hit_rate = box_hits / len(results_with_odds)
    box_roi = box_return / box_investment

    print(f"的中数: {box_hits}/{len(results_with_odds)}")
    print(f"的中率: {box_hit_rate:.2%}")
    print(f"総投資額: {box_investment:,}円")
    print(f"総払戻: {box_return:,}円")
    print(f"収支: {box_return - box_investment:,}円")
    print(f"ROI: {box_roi:.2%}")

    # 分析5: 順位別的中率
    print(f"\n【分析5】順位別的中率")
    print("-" * 50)

    hit_1st = (results_with_odds['predicted_1st'] == results_with_odds['actual_1st']).mean()
    hit_2nd = (results_with_odds['predicted_2nd'] == results_with_odds['actual_2nd']).mean()
    hit_3rd = (results_with_odds['predicted_3rd'] == results_with_odds['actual_3rd']).mean()

    print(f"1着的中率: {hit_1st:.2%}")
    print(f"2着的中率: {hit_2nd:.2%}")
    print(f"3着的中率: {hit_3rd:.2%}")

    # 分析6: 上位2頭的中率
    print(f"\n【分析6】上位2頭的中率（順不同）")
    print("-" * 50)

    top2_hits = 0
    for _, row in results_with_odds.iterrows():
        pred_top2 = {row['predicted_1st'], row['predicted_2nd']}
        actual_top2 = {row['actual_1st'], row['actual_2nd']}
        if pred_top2 == actual_top2:
            top2_hits += 1

    top2_hit_rate = top2_hits / len(results_with_odds)
    print(f"上位2頭的中率: {top2_hit_rate:.2%}")

    print("\n=== 分析完了 ===")


if __name__ == "__main__":
    main()
