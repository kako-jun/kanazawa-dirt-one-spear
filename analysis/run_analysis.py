#!/usr/bin/env python3
"""
分析実行スクリプト（結果をdocsに保存）
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

# プロジェクトルート
PROJECT_ROOT = Path(__file__).parent.parent
ANALYSIS_DIR = Path(__file__).parent
DOCS_DIR = PROJECT_ROOT / "docs"


def run_basic_stats():
    """基本統計分析を実行してファイルに保存"""
    print("=" * 80)
    print("基本統計分析を実行中...")
    print("=" * 80)

    # 実行
    result = subprocess.run(
        [sys.executable, ANALYSIS_DIR / "basic_stats.py"],
        capture_output=True,
        text=True,
    )

    # 結果を表示
    print(result.stdout)
    if result.stderr:
        print("エラー:", result.stderr, file=sys.stderr)

    # ファイルに保存
    output_dir = DOCS_DIR / "basic-stats"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{datetime.now().strftime('%Y-%m-%d')}_basic_stats.md"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# 金沢競馬データ基本統計分析\n\n")
        f.write(f"**実行日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("```\n")
        f.write(result.stdout)
        f.write("\n```\n")

    print(f"\n✅ 結果を保存しました: {output_file}")
    return output_file


def run_benfords_law():
    """ベンフォードの法則分析を実行してファイルに保存"""
    print("\n" + "=" * 80)
    print("ベンフォードの法則による公平性検証を実行中...")
    print("=" * 80)

    # 実行
    result = subprocess.run(
        [sys.executable, ANALYSIS_DIR / "benfords_law.py"],
        capture_output=True,
        text=True,
    )

    # 結果を表示
    print(result.stdout)
    if result.stderr:
        print("エラー:", result.stderr, file=sys.stderr)

    # ファイルに保存
    output_dir = DOCS_DIR / "fairness"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{datetime.now().strftime('%Y-%m-%d')}_benfords_law.md"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# ベンフォードの法則による公平性検証\n\n")
        f.write(f"**実行日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("```\n")
        f.write(result.stdout)
        f.write("\n```\n")
        if result.stderr:
            f.write("\n## エラー・警告\n\n")
            f.write("```\n")
            f.write(result.stderr)
            f.write("\n```\n")

    print(f"\n✅ 結果を保存しました: {output_file}")
    return output_file


def main():
    """メイン実行"""
    print("金沢競馬データ分析実行")
    print(f"プロジェクトルート: {PROJECT_ROOT}")
    print(f"ドキュメント保存先: {DOCS_DIR}")
    print()

    # 各分析を実行
    results = []

    try:
        results.append(run_basic_stats())
    except Exception as e:
        print(f"❌ 基本統計分析でエラー: {e}", file=sys.stderr)

    try:
        results.append(run_benfords_law())
    except Exception as e:
        print(f"❌ ベンフォードの法則分析でエラー: {e}", file=sys.stderr)

    # サマリー
    print("\n" + "=" * 80)
    print("分析完了")
    print("=" * 80)
    print(f"\n保存されたファイル:")
    for result_file in results:
        if result_file:
            print(f"  - {result_file}")


if __name__ == "__main__":
    main()
