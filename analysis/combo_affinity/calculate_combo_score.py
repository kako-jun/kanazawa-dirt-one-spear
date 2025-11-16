#!/usr/bin/env python3
"""
馬×騎手コンビスコア計算スクリプト
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "backend"))

from app.database import SessionLocal, DB_PATH


def calculate_combo_score(horse_id, jockey_id, db):
    """
    馬×騎手のコンビスコアを計算

    Args:
        horse_id: 馬ID
        jockey_id: 騎手ID
        db: Database session

    Returns:
        combo_score: 0-1のスコア
    """
    # stat_horse_jockey_comboから取得
    query = """
    SELECT
        win_rate,
        place_rate,
        total_races,
        avg_finish_position
    FROM stat_horse_jockey_combo
    WHERE horse_id = ? AND jockey_id = ?
    """

    result = db.execute(query, (horse_id, jockey_id)).fetchone()

    if result is None or result[2] < 3:  # 経験回数が3回未満
        return 0.0

    win_rate, place_rate, total_races, avg_finish = result

    # コンビスコア計算
    score = (
        0.5 * win_rate +
        0.3 * place_rate +
        0.2 * (1 / avg_finish if avg_finish > 0 else 0)
    )

    # 経験回数によるボーナス
    experience_bonus = min(total_races / 10, 1.0) * 0.1
    score = min(score + experience_bonus, 1.0)

    return score


def analyze_all_combos():
    """全コンビのスコアを分析"""
    print("=" * 80)
    print("Combo Affinity: コンビスコア計算")
    print("=" * 80)
    print(f"DB: {DB_PATH}")
    print()

    db = SessionLocal()

    try:
        query = """
        SELECT
            horse_id,
            jockey_id,
            win_rate,
            place_rate,
            total_races,
            avg_finish_position
        FROM stat_horse_jockey_combo
        WHERE total_races >= 3
        ORDER BY win_rate DESC
        """

        df = pd.read_sql(query, db.connection())
        print(f"✅ コンビデータ取得: {len(df):,}件")
        print()

        # スコア計算
        df['combo_score'] = df.apply(
            lambda row: (
                0.5 * row['win_rate'] +
                0.3 * row['place_rate'] +
                0.2 * (1 / row['avg_finish_position'] if row['avg_finish_position'] > 0 else 0)
            ),
            axis=1
        )

        # 経験ボーナス
        df['experience_bonus'] = df['total_races'].apply(lambda x: min(x / 10, 1.0) * 0.1)
        df['combo_score'] = (df['combo_score'] + df['experience_bonus']).clip(upper=1.0)

        # 統計
        print("コンビスコア統計:")
        print(df['combo_score'].describe())
        print()

        print("トップ20の黄金コンビ:")
        print(df.nlargest(20, 'combo_score')[['horse_id', 'jockey_id', 'total_races', 'win_rate', 'combo_score']])
        print()

        # 保存
        output_path = project_root / "analysis" / "output" / "combo_scores.csv"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"✅ コンビスコアを保存: {output_path}")

        return df

    finally:
        db.close()


if __name__ == "__main__":
    df = analyze_all_combos()

    print()
    print("=" * 80)
    print("完了")
    print("=" * 80)
