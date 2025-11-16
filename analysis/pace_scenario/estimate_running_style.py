#!/usr/bin/env python3
"""
脚質推定スクリプト

コーナー通過順から各馬の脚質（逃げ/先行/差し/追込）を推定する
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "backend"))

from app.database import SessionLocal, DB_PATH


def estimate_running_style(c1, c2, c3, c4, finish_position):
    """
    コーナー通過順から脚質を推定

    Args:
        c1-c4: 各コーナーの通過順
        finish_position: 最終着順

    Returns:
        running_style: 逃げ/先行/差し/追込
    """
    if pd.isna(c1) or pd.isna(c2):
        return None

    # 前半（1-2コーナー）の平均順位
    early_position = (c1 + c2) / 2

    # 後半（3-4コーナー）の平均順位（欠損の場合は前半と同じと仮定）
    if pd.isna(c3) or pd.isna(c4):
        late_position = early_position
    else:
        late_position = (c3 + c4) / 2

    # 追い上げ度
    closing_power = early_position - late_position

    # 脚質判定
    if early_position <= 2:
        return "逃げ"
    elif early_position <= 5:
        if closing_power < -1:
            return "先行"
        else:
            return "差し"
    else:
        if closing_power > 2:
            return "追込"
        else:
            return "差し"


def analyze_running_styles():
    """全レースの脚質を推定"""
    print("=" * 80)
    print("Pace Scenario: 脚質推定")
    print("=" * 80)
    print(f"DB: {DB_PATH}")
    print()

    db = SessionLocal()

    try:
        query = """
        SELECT
            race_id,
            horse_id,
            corner_1_position,
            corner_2_position,
            corner_3_position,
            corner_4_position,
            finish_position
        FROM race_performances
        WHERE corner_1_position IS NOT NULL
          AND corner_2_position IS NOT NULL
        ORDER BY race_id, corner_1_position
        """

        df = pd.read_sql(query, db.connection())
        print(f"✅ データ取得完了: {len(df):,}件")

        if len(df) == 0:
            print("⚠️  コーナー通過順データが存在しません")
            print("   pace-scenario作戦は実装できません")
            return None

        print(f"   データ充足率: {len(df) / 76879 * 100:.1f}%")  # 76,879 = 全race_performances
        print()

        # 脚質推定
        df['running_style'] = df.apply(
            lambda row: estimate_running_style(
                row['corner_1_position'],
                row['corner_2_position'],
                row['corner_3_position'],
                row['corner_4_position'],
                row['finish_position'],
            ),
            axis=1
        )

        # 統計
        print("脚質分布:")
        print(df['running_style'].value_counts())
        print()

        print("脚質別の平均着順:")
        avg_finish = df.groupby('running_style')['finish_position'].mean().sort_values()
        print(avg_finish)
        print()

        # 保存
        output_path = project_root / "analysis" / "output" / "running_styles.csv"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"✅ 脚質データを保存: {output_path}")

        return df

    finally:
        db.close()


if __name__ == "__main__":
    df = analyze_running_styles()

    if df is not None:
        print()
        print("=" * 80)
        print("完了")
        print("=" * 80)
