#!/usr/bin/env python3
"""
コースレコードHTMLをパースしてJSONに変換
"""
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup


def parse_time_to_seconds(time_str: str) -> float:
    """
    タイム文字列を秒数に変換
    例: "0:53.6" -> 53.6, "1:21.9" -> 81.9
    """
    parts = time_str.split(':')
    if len(parts) == 2:
        minutes = int(parts[0])
        seconds = float(parts[1])
        return minutes * 60 + seconds
    return float(time_str)


def parse_course_records(html_path: Path) -> dict:
    """
    コースレコードHTMLをパースする

    Returns:
        {
            "course": "金沢",
            "direction": "右回り",
            "records": [
                {
                    "distance": 900,
                    "record_time": "0:53.6",
                    "record_seconds": 53.6,
                    "horse_name": "ニュータウンガール",
                    "jockey_name": "○○",
                    "achieved_date": "2021-06-29"
                },
                ...
            ]
        }
    """
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    result = {
        "course": "金沢",
        "direction": "右回り",
        "records": []
    }

    # 金沢のコースレコード行を探す（class="courseRecord__record js-course-kana"）
    rows = soup.find_all('tr', class_='js-course-kana')

    for row in rows:
        cells = row.find_all('td')
        if len(cells) < 7:
            continue

        # セル構造: [競馬場, 回り, 距離, タイム, 馬名, 騎手名, 日付]
        course_name = cells[0].get_text(strip=True)
        direction = cells[1].get_text(strip=True)
        distance_str = cells[2].get_text(strip=True)
        record_time = cells[3].get_text(strip=True)
        horse_name = cells[4].get_text(strip=True)
        jockey_full = cells[5].get_text(strip=True)
        date_str = cells[6].get_text(strip=True)

        # 距離を抽出（例: "900m" -> 900）
        distance_match = re.search(r'(\d+)', distance_str)
        if not distance_match:
            continue
        distance = int(distance_match.group(1))

        # タイムを秒数に変換
        record_seconds = parse_time_to_seconds(record_time)

        # 騎手名から読みがなを除去（例: "岡部　誠オカベ　マコト" -> "岡部　誠"）
        jockey_name = re.sub(r'[ァ-ヴー\s]+$', '', jockey_full).strip()

        # 日付を正規化（YYYY/MM/DD -> YYYY-MM-DD）
        date_match = re.search(r'(\d{4})/(\d{1,2})/(\d{1,2})', date_str)
        if date_match:
            year, month, day = date_match.groups()
            achieved_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        else:
            achieved_date = date_str

        record = {
            "distance": distance,
            "record_time": record_time,
            "record_seconds": record_seconds,
            "horse_name": horse_name,
            "jockey_name": jockey_name,
            "achieved_date": achieved_date
        }
        result["records"].append(record)

    # 距離順にソート
    result["records"].sort(key=lambda x: x["distance"])

    return result


def main():
    html_path = Path("data/reference_data/html/course_records.html")
    json_path = Path("data/reference_data/json/course_records.json")

    if not html_path.exists():
        print(f"HTMLファイルが見つかりません: {html_path}")
        return

    print(f"パース中: {html_path}")
    data = parse_course_records(html_path)

    # JSONディレクトリを作成
    json_path.parent.mkdir(parents=True, exist_ok=True)

    # JSON保存
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"保存完了: {json_path}")
    print(f"レコード数: {len(data['records'])}")

    # サマリー表示
    print("\n距離別レコード:")
    for record in data["records"]:
        print(f"  {record['distance']:4d}m: {record['record_time']} "
              f"({record['horse_name'] or '不明'}, "
              f"{record['jockey_name'] or '不明'}, "
              f"{record['achieved_date'] or '不明'})")


if __name__ == "__main__":
    main()
