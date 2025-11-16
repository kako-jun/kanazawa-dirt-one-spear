#!/usr/bin/env python3
"""
全ての3連単組み合わせを生成
"""

import sys
from pathlib import Path
from itertools import permutations
import pandas as pd

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "backend"))

from app.database import SessionLocal, DB_PATH


def generate_all_triplets_for_race(race_id, db):
    """
    レース内の全ての3連単組み合わせを生成

    Args:
        race_id: レースID
        db: Database session

    Returns:
        list of triplets
    """
    # レース内の馬を取得
    query = """
    SELECT
        horse_id,
        horse_number,
        gate_number,
        popularity
    FROM race_performances
    WHERE race_id = ?
    ORDER BY horse_number
    """

    horses = pd.read_sql(query, db.connection(), params=(race_id,))

    if len(horses) < 3:
        print(f"⚠️  レース{race_id}: 馬が3頭未満")
        return []

    # 全ての順列を生成（順序が重要）
    horse_ids = horses['horse_id'].tolist()
    triplets = list(permutations(horse_ids, 3))

    print(f"レース{race_id}: {len(horses)}頭 → {len(triplets)}通りの組み合わせ")

    return triplets


def generate_all_triplets():
    """全レースの組み合わせを生成"""
    print("=" * 80)
    print("Triplet Combination: 全組み合わせ生成")
    print("=" * 80)
    print(f"DB: {DB_PATH}")
    print()

    db = SessionLocal()

    try:
        # 全レースを取得
        query = "SELECT DISTINCT id FROM races ORDER BY id LIMIT 100"  # テスト用に100レースに限定
        race_ids = pd.read_sql(query, db.connection())['id'].tolist()

        print(f"対象レース数: {len(race_ids):,}件")
        print()

        all_triplets = []

        for race_id in race_ids:
            triplets = generate_all_triplets_for_race(race_id, db)

            for triplet in triplets:
                all_triplets.append({
                    'race_id': race_id,
                    'horse1_id': triplet[0],
                    'horse2_id': triplet[1],
                    'horse3_id': triplet[2],
                })

        df = pd.DataFrame(all_triplets)
        print()
        print(f"✅ 総組み合わせ数: {len(df):,}件")

        # 保存
        output_path = project_root / "analysis" / "output" / "all_triplets.csv"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"✅ 組み合わせデータを保存: {output_path}")

        return df

    finally:
        db.close()


if __name__ == "__main__":
    df = generate_all_triplets()

    print()
    print("=" * 80)
    print("完了")
    print("=" * 80)
