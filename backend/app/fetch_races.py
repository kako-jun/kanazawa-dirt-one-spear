"""
金沢競馬のレースデータ取得スクリプト

使い方:
  # 未来のレース（今月と来月の出馬表）
  python -m app.fetch_races --future

  # 過去のレース結果（先月）
  python -m app.fetch_races --past

  # 特定の日付のレース
  python -m app.fetch_races --date 2025-01-15
"""
import argparse
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.database import SessionLocal, init_db
from app.scrapers.nar_scraper import NARScraper
from app import crud
from app.predictor import generate_simple_prediction


def fetch_future_races():
    """未来のレース（出馬表）を取得"""
    print("=== 未来のレース取得開始 ===")

    init_db()
    db = SessionLocal()
    scraper = NARScraper()

    try:
        today = datetime.now()

        # 今月と来月の開催日を取得
        for month_offset in [0, 1]:
            target_date = today + timedelta(days=30 * month_offset)
            year = target_date.year
            month = target_date.month

            print(f"\n{year}年{month}月の金沢競馬開催日を取得中...")
            race_dates = scraper.get_race_dates(year, month)
            print(f"  → {len(race_dates)}日の開催を発見")

            # 未来の日付のみ
            future_dates = [d for d in race_dates if d.date() >= today.date()]

            for race_date in future_dates:
                print(f"\n{race_date.strftime('%Y-%m-%d')} のレース取得中...")

                # レース番号一覧取得
                race_numbers = scraper.get_race_list(race_date)
                print(f"  → {len(race_numbers)}レースを発見")

                for race_no in race_numbers:
                    # 既に登録済みかチェック
                    race_id = f"race_{race_date.strftime('%Y%m%d')}_{race_no:02d}"
                    existing_race = crud.get_race(db, race_id)

                    if existing_race:
                        print(f"    {race_no}R: スキップ（既存）")
                        continue

                    # 出馬表取得
                    race = scraper.scrape_race(race_date, race_no)

                    if race:
                        # DB登録
                        crud.create_race(db, race)
                        print(f"    {race_no}R: {race.name} - {len(race.entries)}頭登録")

                        # 予想生成
                        prediction = generate_simple_prediction(race)
                        crud.create_prediction(db, prediction)
                        print(f"    → 予想生成: {prediction.first}-{prediction.second}-{prediction.third}")
                    else:
                        print(f"    {race_no}R: 取得失敗")

        print("\n=== 未来のレース取得完了 ===")

    finally:
        scraper.close()
        db.close()


def fetch_past_results():
    """過去のレース結果を取得"""
    print("=== 過去のレース結果取得開始 ===")

    init_db()
    db = SessionLocal()
    scraper = NARScraper()

    try:
        today = datetime.now()

        # 先月の開催日を取得
        last_month = today - timedelta(days=30)
        year = last_month.year
        month = last_month.month

        print(f"\n{year}年{month}月の金沢競馬結果を取得中...")
        race_dates = scraper.get_race_dates(year, month)

        # 過去の日付のみ
        past_dates = [d for d in race_dates if d.date() < today.date()]
        print(f"  → {len(past_dates)}日の結果を取得")

        for race_date in past_dates:
            print(f"\n{race_date.strftime('%Y-%m-%d')} の結果取得中...")

            race_numbers = scraper.get_race_list(race_date)

            for race_no in race_numbers:
                race_id = f"race_{race_date.strftime('%Y%m%d')}_{race_no:02d}"

                # レース結果取得
                result_data = scraper.scrape_result(race_date, race_no)

                if result_data and result_data['first']:
                    print(f"    {race_no}R: {result_data['first']}-{result_data['second']}-{result_data['third']}")

                    # レースが登録されていなければ取得
                    race = crud.get_race(db, race_id)
                    if not race:
                        race = scraper.scrape_race(race_date, race_no)
                        if race:
                            crud.create_race(db, race)
                            prediction = generate_simple_prediction(race)
                            crud.create_prediction(db, prediction)

                    # 結果をResultSubmitとして登録はしない（管理者が手動で記録すべき）
                    print(f"    → 結果確認済み（手動記録が必要）")
                else:
                    print(f"    {race_no}R: 結果取得失敗")

        print("\n=== 過去のレース結果取得完了 ===")
        print("※ 結果の記録は管理画面から手動で行ってください")

    finally:
        scraper.close()
        db.close()


def fetch_specific_date(date_str: str):
    """特定日付のレースを取得"""
    print(f"=== {date_str} のレース取得開始 ===")

    init_db()
    db = SessionLocal()
    scraper = NARScraper()

    try:
        race_date = datetime.strptime(date_str, '%Y-%m-%d')

        race_numbers = scraper.get_race_list(race_date)
        print(f"  → {len(race_numbers)}レースを発見")

        for race_no in race_numbers:
            race_id = f"race_{race_date.strftime('%Y%m%d')}_{race_no:02d}"

            # 既存チェック
            existing_race = crud.get_race(db, race_id)
            if existing_race:
                print(f"  {race_no}R: スキップ（既存）")
                continue

            # 出馬表取得
            race = scraper.scrape_race(race_date, race_no)

            if race:
                crud.create_race(db, race)
                print(f"  {race_no}R: {race.name} - {len(race.entries)}頭登録")

                prediction = generate_simple_prediction(race)
                crud.create_prediction(db, prediction)
                print(f"  → 予想: {prediction.first}-{prediction.second}-{prediction.third}")

        print(f"\n=== {date_str} のレース取得完了 ===")

    finally:
        scraper.close()
        db.close()


def main():
    parser = argparse.ArgumentParser(description='金沢競馬データ取得')
    parser.add_argument('--future', action='store_true', help='未来のレース（出馬表）を取得')
    parser.add_argument('--past', action='store_true', help='過去のレース結果を取得')
    parser.add_argument('--date', type=str, help='特定日付のレース取得 (YYYY-MM-DD)')

    args = parser.parse_args()

    if args.future:
        fetch_future_races()
    elif args.past:
        fetch_past_results()
    elif args.date:
        fetch_specific_date(args.date)
    else:
        print("使い方:")
        print("  未来のレース: python -m app.fetch_races --future")
        print("  過去の結果:   python -m app.fetch_races --past")
        print("  特定日付:     python -m app.fetch_races --date 2025-01-15")


if __name__ == "__main__":
    main()
