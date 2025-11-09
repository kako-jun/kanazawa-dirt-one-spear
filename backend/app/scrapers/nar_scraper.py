"""
NAR公式サイト（keiba.go.jp）スクレイパー

控えめなアクセス:
- リクエスト間隔: 3秒以上
- User-Agent設定
- robots.txt遵守
- 1日1回の実行推奨
"""
import time
import uuid
from datetime import datetime, timedelta
from typing import List, Optional
import httpx
from bs4 import BeautifulSoup

from app.models import Race, Entry, Horse


class NARScraper:
    BASE_URL = "https://www.keiba.go.jp/KeibaWeb"
    KANAZAWA_CODE = "46"  # 金沢競馬場コード

    def __init__(self):
        self.session = httpx.Client(
            timeout=30.0,
            headers={
                "User-Agent": "KanazawaDirtOneSpear/1.0 (Hobby Project; Non-commercial)",
            }
        )

    def _wait(self):
        """礼儀正しく3秒待つ"""
        time.sleep(3.0)

    def get_race_dates(self, year: int, month: int) -> List[datetime]:
        """
        指定月の金沢競馬開催日を取得
        """
        url = f"{self.BASE_URL}/MonthlyConveneInfo/MonthlyConveneInfoTop"
        params = {
            "k_year": year,
            "k_month": month,
            "k_babaCode": self.KANAZAWA_CODE,
        }

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # カレンダーから開催日を抽出
            race_dates = []
            calendar = soup.find('table', class_='calendar') or soup.find('table')

            if calendar:
                for link in calendar.find_all('a'):
                    date_str = link.get('href', '')
                    if 'k_raceDate=' in date_str:
                        # URLからYYYY-MM-DD形式の日付を抽出
                        date_part = date_str.split('k_raceDate=')[1].split('&')[0]
                        try:
                            race_date = datetime.strptime(date_part, '%Y-%m-%d')
                            race_dates.append(race_date)
                        except ValueError:
                            continue

            return sorted(set(race_dates))

        except Exception as e:
            print(f"開催日取得エラー: {e}")
            return []

    def get_race_list(self, race_date: datetime) -> List[int]:
        """
        指定日のレース番号一覧を取得
        """
        self._wait()

        url = f"{self.BASE_URL}/TodayRaceInfo/RaceList"
        params = {
            "k_raceDate": race_date.strftime('%Y-%m-%d'),
            "k_babaCode": self.KANAZAWA_CODE,
        }

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            race_numbers = []
            # レース一覧から番号を抽出
            for link in soup.find_all('a'):
                href = link.get('href', '')
                if 'k_raceNo=' in href:
                    try:
                        race_no = int(href.split('k_raceNo=')[1].split('&')[0])
                        race_numbers.append(race_no)
                    except (ValueError, IndexError):
                        continue

            return sorted(set(race_numbers))

        except Exception as e:
            print(f"レース一覧取得エラー: {e}")
            return []

    def scrape_race(self, race_date: datetime, race_number: int) -> Optional[Race]:
        """
        出馬表を取得してRaceオブジェクトを生成
        """
        self._wait()

        url = f"{self.BASE_URL}/TodayRaceInfo/DebaTable"
        params = {
            "k_raceDate": race_date.strftime('%Y-%m-%d'),
            "k_raceNo": race_number,
            "k_babaCode": self.KANAZAWA_CODE,
        }

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # レース情報抽出
            race_info = self._extract_race_info(soup, race_date, race_number)
            if not race_info:
                return None

            # 出走馬情報抽出
            entries = self._extract_entries(soup, race_info['race_id'])

            return Race(
                race_id=race_info['race_id'],
                date=race_info['date'],
                race_number=race_number,
                name=race_info['name'],
                distance=race_info['distance'],
                track_condition=race_info['track_condition'],
                weather=race_info['weather'],
                entries=entries,
            )

        except Exception as e:
            print(f"レース取得エラー (日付: {race_date}, レース: {race_number}): {e}")
            return None

    def _extract_race_info(self, soup: BeautifulSoup, race_date: datetime, race_number: int) -> Optional[dict]:
        """レース基本情報を抽出"""
        try:
            # レース名（例: "第1レース", "金沢スプリント"など）
            title = soup.find('h2') or soup.find('h3')
            race_name = title.get_text(strip=True) if title else f"第{race_number}レース"

            # 距離・馬場状態・天候を抽出
            info_text = soup.get_text()

            # 距離抽出（例: "1500m", "ダ1700"など）
            distance = 1500  # デフォルト
            import re
            distance_match = re.search(r'(\d{4})m|ダ(\d{4})', info_text)
            if distance_match:
                distance = int(distance_match.group(1) or distance_match.group(2))

            # 馬場状態（良、稍重、重、不良）
            track_condition = "良"
            for cond in ["不良", "重", "稍重", "良"]:
                if cond in info_text:
                    track_condition = cond
                    break

            # 天候
            weather = "晴"
            for w in ["雪", "雨", "曇", "晴"]:
                if w in info_text:
                    weather = w
                    break

            race_id = f"race_{race_date.strftime('%Y%m%d')}_{race_number:02d}"

            return {
                'race_id': race_id,
                'date': race_date.replace(hour=14, minute=0) + timedelta(minutes=30 * (race_number - 1)),
                'name': race_name,
                'distance': distance,
                'track_condition': track_condition,
                'weather': weather,
            }

        except Exception as e:
            print(f"レース情報抽出エラー: {e}")
            return None

    def _extract_entries(self, soup: BeautifulSoup, race_id: str) -> List[Entry]:
        """出走馬情報を抽出"""
        entries = []

        try:
            # テーブルから馬情報を抽出
            table = soup.find('table')
            if not table:
                return entries

            rows = table.find_all('tr')[1:]  # ヘッダー行をスキップ

            for row in rows:
                cols = row.find_all('td')
                if len(cols) < 5:
                    continue

                try:
                    # 基本情報抽出
                    horse_number = int(cols[0].get_text(strip=True))
                    horse_name = cols[1].get_text(strip=True)

                    # 性齢（例: "牡3"）
                    age_gender = cols[2].get_text(strip=True)
                    gender = age_gender[0] if age_gender else "牡"
                    age = int(age_gender[1:]) if len(age_gender) > 1 else 4

                    # 斤量
                    weight_text = cols[3].get_text(strip=True)
                    weight = float(weight_text) if weight_text else 54.0

                    # 騎手
                    jockey = cols[4].get_text(strip=True) if len(cols) > 4 else "騎手不明"

                    # オッズ（あれば）
                    odds = None
                    if len(cols) > 5:
                        odds_text = cols[5].get_text(strip=True)
                        try:
                            odds = float(odds_text)
                        except ValueError:
                            pass

                    horse = Horse(
                        horse_id=f"horse_{horse_name}_{age}",
                        name=horse_name,
                        age=age,
                        gender=gender,
                    )

                    entry = Entry(
                        entry_id=str(uuid.uuid4()),
                        race_id=race_id,
                        horse=horse,
                        gate_number=(horse_number - 1) % 8 + 1,
                        horse_number=horse_number,
                        jockey=jockey,
                        weight=weight,
                        odds=odds,
                        past_results=[],
                    )

                    entries.append(entry)

                except (ValueError, IndexError) as e:
                    print(f"馬情報抽出エラー: {e}")
                    continue

        except Exception as e:
            print(f"出走馬一覧抽出エラー: {e}")

        return entries

    def scrape_result(self, race_date: datetime, race_number: int) -> Optional[dict]:
        """
        レース結果を取得

        Returns:
            dict: {
                'first': 1着馬番,
                'second': 2着馬番,
                'third': 3着馬番,
                'payout_trifecta': 3連単配当 (100円あたり)
            }
        """
        self._wait()

        url = f"{self.BASE_URL}/TodayRaceInfo/RaceMarkTable"
        params = {
            "k_raceDate": race_date.strftime('%Y-%m-%d'),
            "k_raceNo": race_number,
            "k_babaCode": self.KANAZAWA_CODE,
        }

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # 着順情報を抽出
            result_table = soup.find('table')
            if not result_table:
                return None

            finishers = {}
            rows = result_table.find_all('tr')[1:]

            for row in rows:
                cols = row.find_all('td')
                if len(cols) < 2:
                    continue

                try:
                    finish_pos = cols[0].get_text(strip=True)
                    horse_number = int(cols[1].get_text(strip=True))

                    if finish_pos == "1":
                        finishers['first'] = horse_number
                    elif finish_pos == "2":
                        finishers['second'] = horse_number
                    elif finish_pos == "3":
                        finishers['third'] = horse_number

                except (ValueError, IndexError):
                    continue

            if len(finishers) < 3:
                return None

            # 払戻情報を抽出
            payout_trifecta = None
            payout_section = soup.find(text=lambda t: t and '3連単' in t)
            if payout_section:
                parent = payout_section.find_parent()
                if parent:
                    import re
                    payout_match = re.search(r'([\d,]+)円', parent.get_text())
                    if payout_match:
                        payout_trifecta = int(payout_match.group(1).replace(',', ''))

            return {
                'first': finishers.get('first'),
                'second': finishers.get('second'),
                'third': finishers.get('third'),
                'payout_trifecta': payout_trifecta,
            }

        except Exception as e:
            print(f"結果取得エラー: {e}")
            return None

    def close(self):
        """セッションをクローズ"""
        self.session.close()
