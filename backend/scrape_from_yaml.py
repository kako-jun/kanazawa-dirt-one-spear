#!/usr/bin/env python3
"""
YAMLスケジュールファイルを読み込んで、レース情報と結果を取得
"""
import sys
import yaml
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from app.scrapers.nar_scraper import NARScraper
from app.database import init_db, SessionLocal
from app import crud


def load_schedule(yaml_file: str) -> dict:
    """YAMLファイルを読み込み"""
    with open(yaml_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def scrape_from_schedule(yaml_file: str, fetch_results: bool = False):
    """
    YAMLスケジュールに基づいてスクレイピング

    Args:
        yaml_file: スケジュールYAMLファイルのパス
        fetch_results: レース結果も取得するか（Trueの場合）
    """
    print("=" * 60)
    print("YAML based scraping")
    print("=" * 60)
    print(f"YAMLファイル: {yaml_file}")
    print(f"結果取得: {'ON' if fetch_results else 'OFF'}")
    print("=" * 60 + "\n")

    # YAMLを読み込み
    schedule = load_schedule(yaml_file)
    year = schedule['year']
    track_name = schedule['track_name']
    track_code = schedule['track_code']
    dates = schedule['schedule']

    print(f"対象: {year}年 {track_name}")
    print(f"開催日数: {len(dates)}日\n")

    # データベース初期化
    init_db()
    db = SessionLocal()

    scraper = NARScraper()

    # 統計
    stats = {
        'total_dates': len(dates),
        'races_scraped': 0,
        'races_saved': 0,
        'results_scraped': 0,
        'results_saved': 0,
        'failed': 0,
        'skipped': 0,
    }

    # 各開催日を処理
    for i, date_info in enumerate(dates, 1):
        date_str = date_info['date']
        weekday = date_info['weekday']
        race_date = datetime.strptime(date_str, '%Y-%m-%d')

        print(f"[{i}/{len(dates)}] {date_str} ({weekday})")
        print("-" * 60)

        # レース番号一覧を取得
        race_numbers = scraper.get_race_list(race_date)
        if not race_numbers:
            print(f"  ⚠️  レース一覧が取得できませんでした")
            stats['failed'] += 1
            print()
            continue

        print(f"  レース数: {len(race_numbers)}R")

        # 各レースを処理
        for race_no in race_numbers:
            race_id = f"race_{race_date.strftime('%Y%m%d')}_{race_no:02d}"

            try:
                # 既存チェック
                existing = crud.get_race(db, race_id)
                if existing:
                    print(f"    R{race_no:2d}: スキップ（既存）", end="")
                    stats['skipped'] += 1

                    # 結果取得モードで、まだ結果がなければ取得
                    if fetch_results:
                        existing_result = crud.get_result(db, race_id)
                        if not existing_result:
                            result_data = scraper.scrape_result(race_date, race_no)
                            if result_data:
                                # TODO: 結果をDBに保存
                                print(" → 結果取得✅")
                                stats['results_scraped'] += 1
                            else:
                                print(" → 結果なし")
                        else:
                            print()
                    else:
                        print()
                    continue

                # 出馬表を取得
                race = scraper.scrape_race(race_date, race_no)
                if not race:
                    print(f"    R{race_no:2d}: ❌ 取得失敗")
                    stats['failed'] += 1
                    continue

                stats['races_scraped'] += 1

                # データベースに保存
                crud.create_race(db, race)
                stats['races_saved'] += 1
                horses_count = len(race.entries)
                print(f"    R{race_no:2d}: ✅ {race.name[:20]} ({horses_count}頭)", end="")

                # 結果取得モード
                if fetch_results:
                    result_data = scraper.scrape_result(race_date, race_no)
                    if result_data:
                        # TODO: 結果をDBに保存する機能を実装
                        print(f" + 結果✅")
                        stats['results_scraped'] += 1
                    else:
                        print(f" - 結果なし")
                else:
                    print()

            except Exception as e:
                print(f"    R{race_no:2d}: ❌ エラー - {e}")
                stats['failed'] += 1

        print()

    scraper.close()
    db.close()

    # 最終統計
    print("=" * 60)
    print("完了")
    print("=" * 60)
    print(f"開催日数:          {stats['total_dates']}日")
    print(f"取得レース数:      {stats['races_scraped']}レース")
    print(f"保存レース数:      {stats['races_saved']}レース")
    print(f"スキップ:          {stats['skipped']}レース")
    if fetch_results:
        print(f"取得結果数:        {stats['results_scraped']}件")
        print(f"保存結果数:        {stats['results_saved']}件")
    print(f"失敗・エラー:      {stats['failed']}件")
    print("=" * 60)

    if stats['races_saved'] > 0:
        print(f"\n🎉 {stats['races_saved']}レースの情報を保存しました！")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='YAMLスケジュールからレース情報を取得')
    parser.add_argument('yaml_file', help='スケジュールYAMLファイル（例: data/2025_schedule.yaml）')
    parser.add_argument('--results', action='store_true', help='レース結果も取得する')

    args = parser.parse_args()

    try:
        scrape_from_schedule(args.yaml_file, fetch_results=args.results)
    except KeyboardInterrupt:
        print("\n\n⚠️  ユーザーによって中断されました")
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        import traceback
        traceback.print_exc()
