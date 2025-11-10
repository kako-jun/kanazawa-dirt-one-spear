#!/usr/bin/env python3
"""
指定年の開催スケジュールをYAML形式で出力
"""
import sys
from pathlib import Path
from datetime import datetime
import yaml

sys.path.insert(0, str(Path(__file__).parent))

from app.scrapers.nar_scraper import NARScraper


def get_schedule_yaml(year: int):
    """指定年の開催スケジュールを取得してYAMLデータを生成"""
    scraper = NARScraper()
    all_dates = []

    print(f"{year}年の開催日を取得中...", file=sys.stderr)
    for month in range(4, 12):
        dates = scraper.get_race_dates(year, month)
        if dates:
            all_dates.extend(dates)

    scraper.close()

    all_dates = sorted(set(all_dates))

    # YAML形式のデータを生成
    weekday_names = ["月", "火", "水", "木", "金", "土", "日"]

    schedule_data = {
        'year': year,
        'track_name': '金沢競馬場',
        'track_code': '22',
        'url_templates': {
            'race_list': 'https://www.keiba.go.jp/KeibaWeb/TodayRaceInfo/RaceList?k_raceDate={date}&k_babaCode={track_code}',
            'deba_table': 'https://www.keiba.go.jp/KeibaWeb/TodayRaceInfo/DebaTable?k_raceDate={date}&k_raceNo={race_no}&k_babaCode={track_code}',
            'result': 'https://www.keiba.go.jp/KeibaWeb/TodayRaceInfo/RaceMarkTable?k_raceDate={date}&k_raceNo={race_no}&k_babaCode={track_code}'
        },
        'schedule': [
            {
                'date': date.strftime('%Y-%m-%d'),
                'weekday': weekday_names[date.weekday()]
            }
            for date in all_dates
        ]
    }

    # 統計情報
    monthly_counts = {}
    weekday_counts = {i: 0 for i in range(7)}

    for date in all_dates:
        month = date.month
        monthly_counts[month] = monthly_counts.get(month, 0) + 1
        weekday_counts[date.weekday()] += 1

    month_names = ['april', 'may', 'june', 'july', 'august', 'september', 'october', 'november']
    weekday_names_en = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    schedule_data['statistics'] = {
        'total_days': len(all_dates),
        'by_month': {month_names[m-4]: monthly_counts.get(m, 0) for m in range(4, 12)},
        'by_weekday': {weekday_names_en[i]: weekday_counts[i] for i in range(7)}
    }

    return schedule_data


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_schedule_for_yaml.py <year>")
        sys.exit(1)

    year = int(sys.argv[1])
    data = get_schedule_yaml(year)

    print(f"# {year}年 金沢競馬 開催スケジュール")
    print(f"# 取得日: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"# ソース: NAR公式サイト (https://www.keiba.go.jp/KeibaWeb)\n")
    print(yaml.dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False))
