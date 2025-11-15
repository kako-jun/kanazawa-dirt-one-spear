#!/usr/bin/env python3
"""
騎手マスターデータをDBに統合

jockeys_kanazawa.yamlから騎手の生年月日、読み仮名、性別をDBに投入
"""

import sqlite3
import yaml
from pathlib import Path
from datetime import datetime


def integrate_jockey_master(db_path: Path, yaml_path: Path):
    """騎手マスターデータをDBに統合"""

    # YAMLを読み込み
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    jockeys = data.get('jockeys', [])
    print(f"読み込んだ騎手数: {len(jockeys)}")

    # DBに接続
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    updated_count = 0
    not_found_count = 0
    skipped_count = 0

    try:
        for jockey in jockeys:
            name = jockey['name']
            birth_date = jockey.get('birth_date')
            furigana = jockey.get('furigana')
            gender = jockey.get('gender')

            # DBで騎手を検索
            # DBには短縮名（姓+名の最初の1文字、スペースなし）が格納されているため、
            # YAMLの完全名からスペースを除去し、部分一致で検索
            name_no_space = name.replace(' ', '')

            # 完全一致を試す
            cursor.execute("SELECT jockey_id, name FROM jockeys WHERE name = ?", (name,))
            result = cursor.fetchone()

            # 完全一致しない場合、DBの短縮名がYAML名のプレフィックスになっているか確認
            if not result:
                cursor.execute("SELECT jockey_id, name FROM jockeys WHERE ? LIKE name || '%'", (name_no_space,))
                result = cursor.fetchone()

            if result:
                jockey_id, db_name = result

                # 既存の騎手を更新
                cursor.execute("""
                    UPDATE jockeys
                    SET birth_date = ?, furigana = ?, gender = ?
                    WHERE jockey_id = ?
                """, (birth_date, furigana, gender, jockey_id))

                updated_count += 1
                print(f"  更新: {name} ({furigana}) → DB名: {db_name}")
            else:
                not_found_count += 1
                print(f"  ⚠️ DBに見つかりません: {name} (金沢所属だが未出走の可能性)")

        conn.commit()

        print(f"\n=== 統合完了 ===")
        print(f"更新: {updated_count}件")
        print(f"DBに未存在: {not_found_count}件")

    except Exception as e:
        conn.rollback()
        print(f"❌ エラー: {e}")
        raise

    finally:
        conn.close()


def main():
    backend_dir = Path(__file__).parent
    db_path = backend_dir / 'data' / 'kanazawa_dirt_one_spear.db'
    yaml_path = backend_dir / 'data' / 'reference_data' / 'yaml' / 'master' / 'jockeys_kanazawa.yaml'

    if not db_path.exists():
        print(f"❌ DBが見つかりません: {db_path}")
        return

    if not yaml_path.exists():
        print(f"❌ YAMLが見つかりません: {yaml_path}")
        return

    print(f"騎手マスターデータ統合")
    print(f"  ソース: {yaml_path.name}")
    print(f"  対象DB: {db_path.name}")
    print()

    integrate_jockey_master(db_path, yaml_path)


if __name__ == '__main__':
    main()
