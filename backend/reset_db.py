#!/usr/bin/env python3
"""
データベースを初期化
"""

from pathlib import Path
from app.database import engine, Base, DB_DIR

DB_PATH = DB_DIR / "kanazawa_dirt_one_spear.db"

print("=" * 80)
print("データベース初期化")
print("=" * 80)
print(f"DB: {DB_PATH}")
print()

# 既存DBを削除
if DB_PATH.exists():
    DB_PATH.unlink()
    print("✅ 既存DBを削除しました")
else:
    print("ℹ️ DBファイルは存在しませんでした")

# 新しいDBを作成
Base.metadata.create_all(bind=engine)
print("✅ 新しいDBを作成しました")

print()
print("=" * 80)
print("初期化完了")
print("=" * 80)
