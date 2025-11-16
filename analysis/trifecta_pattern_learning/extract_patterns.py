#!/usr/bin/env python3
"""
過去の3連単パターンを抽出
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from collections import Counter

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "backend"))

from app.database import SessionLocal, DB_PATH


def extract_trifecta_patterns():
    """過去の3連単パターンを抽出"""
    print("=" * 80)
    print("Trifecta Pattern Learning: パターン抽出")
    print("=" * 80)
    print(f"DB: {DB_PATH}")
    print()

    db = SessionLocal()

    try:
        # 過去の3連単結果を取得
        query = """
        SELECT
            r.id as race_id,
            r.race_date,
            r.track_condition,
            r.distance,

            -- 1-2-3着の人気順位
            (SELECT popularity FROM race_performances
             WHERE race_id = r.id AND finish_position = 1) as first_popularity,
            (SELECT popularity FROM race_performances
             WHERE race_id = r.id AND finish_position = 2) as second_popularity,
            (SELECT popularity FROM race_performances
             WHERE race_id = r.id AND finish_position = 3) as third_popularity,

            -- 3連単配当
            (SELECT payout FROM payouts
             WHERE race_id = r.id AND payout_type = 'trifecta'
             LIMIT 1) as trifecta_payout

        FROM races r
        WHERE r.id IN (SELECT DISTINCT race_id FROM race_performances WHERE finish_position <= 3)
        ORDER BY r.race_date
        """

        df = pd.read_sql(query, db.connection())
        print(f"✅ データ取得: {len(df):,}レース")
        print()

        # 人気パターンを作成
        df['popularity_pattern'] = df.apply(
            lambda row: f"{int(row['first_popularity'])}-{int(row['second_popularity'])}-{int(row['third_popularity'])}"
            if pd.notna(row['first_popularity']) else None,
            axis=1
        )

        # 万馬券フラグ
        df['is_万馬券'] = df['trifecta_payout'] >= 10000

        # パターン頻度分析
        print("=" * 80)
        print("人気パターン頻度 トップ20:")
        print("=" * 80)

        pattern_counter = Counter(df['popularity_pattern'].dropna())
        for pattern, count in pattern_counter.most_common(20):
            frequency = count / len(df)
            avg_payout = df[df['popularity_pattern'] == pattern]['trifecta_payout'].mean()

            print(f"{pattern}: {frequency:.2%} ({count}回) 平均配当{avg_payout:,.0f}円")

        print()

        # 万馬券パターン
        print("=" * 80)
        print("万馬券パターン（配当10,000円以上）:")
        print("=" * 80)

        万馬券_df = df[df['is_万馬券'] == True]
        万馬券_pattern_counter = Counter(万馬券_df['popularity_pattern'].dropna())

        for pattern, count in 万馬券_pattern_counter.most_common(20):
            frequency = count / len(万馬券_df)
            avg_payout = 万馬券_df[万馬券_df['popularity_pattern'] == pattern]['trifecta_payout'].mean()

            print(f"{pattern}: {frequency:.2%} ({count}回) 平均配当{avg_payout:,.0f}円")

        print()

        # 保存
        output_path = project_root / "analysis" / "output" / "trifecta_patterns.csv"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"✅ パターンデータを保存: {output_path}")

        return df

    finally:
        db.close()


if __name__ == "__main__":
    df = extract_trifecta_patterns()

    print()
    print("=" * 80)
    print("完了")
    print("=" * 80)
