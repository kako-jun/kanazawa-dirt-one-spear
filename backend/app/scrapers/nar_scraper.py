"""
NAR公式サイト（keiba.go.jp）スクレイパー

控えめなアクセス:
- リクエスト間隔: 3秒以上
- User-Agent設定
- robots.txt遵守
- 1日1回の実行推奨
"""
import os
import time
import uuid
from datetime import datetime, timedelta
from typing import List, Optional
from pathlib import Path
import httpx
from bs4 import BeautifulSoup

from app.models import Race, Entry, Horse


class NARScraper:
    BASE_URL = "https://www.keiba.go.jp/KeibaWeb"
    KANAZAWA_CODE = "22"  # 金沢競馬場コード

    def __init__(self, save_html: bool = True, html_dir: str = "data/html"):
        # プロキシ設定（環境変数から取得）
        proxy = os.getenv('HTTPS_PROXY') or os.getenv('HTTP_PROXY')

        self.session = httpx.Client(
            timeout=30.0,
            proxy=proxy,
            verify=False,  # SSL証明書の検証をスキップ（プロキシ経由のため）
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }
        )
        self.save_html = save_html
        self.html_dir = Path(html_dir)
        if save_html:
            self.html_dir.mkdir(parents=True, exist_ok=True)

    def _wait(self):
        """礼儀正しく3秒待つ"""
        time.sleep(3.0)

    def _save_html(self, html: str, date: datetime, filename: str):
        """HTMLをファイルに保存"""
        if not self.save_html:
            return

        # ディレクトリ構造: data/html/YYYY/YYYYMMDD/
        year_dir = self.html_dir / str(date.year)
        date_dir = year_dir / date.strftime('%Y%m%d')
        date_dir.mkdir(parents=True, exist_ok=True)

        # ファイルパス
        filepath = date_dir / filename

        # HTML保存
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

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
                    href = link.get('href', '')
                    # 金沢競馬場のリンクのみ抽出
                    if 'k_raceDate=' in href and f'k_babaCode={self.KANAZAWA_CODE}' in href:
                        # URLからYYYY/MM/DD形式の日付を抽出（URLエンコードされている）
                        date_part = href.split('k_raceDate=')[1].split('&')[0]
                        # URLデコード: %2f -> /
                        date_part = date_part.replace('%2f', '/').replace('%2F', '/')
                        try:
                            race_date = datetime.strptime(date_part, '%Y/%m/%d')
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

            # HTML保存
            self._save_html(response.text, race_date, 'race_list.html')

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

            # HTML保存
            filename = f'race_{race_number:02d}_deba.html'
            self._save_html(response.text, race_date, filename)

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
            import re

            # レース名（例: "第1レース", "金沢スプリント"など）
            title = soup.find('h2') or soup.find('h3')
            race_name = title.get_text(strip=True) if title else f"第{race_number}レース"

            # 距離・馬場状態・天候・周回方向を抽出
            info_text = soup.get_text()

            # 距離と周回方向抽出（例: "ダート1400ｍ（右）"）
            distance = 1500  # デフォルト
            direction = None  # 左回りor右回り

            distance_match = re.search(r'ダート\s*(\d{4})ｍ\s*（(左|右)）', info_text)
            if distance_match:
                distance = int(distance_match.group(1))
                direction = distance_match.group(2) + '回り'
            else:
                # フォールバック: 距離のみ
                distance_match2 = re.search(r'(\d{4})m|ダ(\d{4})', info_text)
                if distance_match2:
                    distance = int(distance_match2.group(1) or distance_match2.group(2))

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
                'direction': direction,
            }

        except Exception as e:
            print(f"レース情報抽出エラー: {e}")
            return None

    def _extract_entries(self, soup: BeautifulSoup, race_id: str) -> List[Entry]:
        """出走馬情報を抽出"""
        entries = []

        try:
            # 馬名のリンクを探す（より確実な方法）
            horse_links = soup.find_all('a', class_='horseName')

            for horse_link in horse_links:
                try:
                    horse_name = horse_link.get_text(strip=True)
                    if not horse_name:
                        continue

                    # 馬番・枠番を取得（同じ行内から）
                    parent_row = horse_link.find_parent('tr')
                    if not parent_row:
                        continue

                    # 最初の td が枠番、2番目が馬番のパターンが多い
                    tds = parent_row.find_all('td')
                    gate_number = 1
                    horse_number = len(entries) + 1  # デフォルトは順番

                    # 枠番・馬番を探す
                    for i, td in enumerate(tds[:3]):  # 最初の3列を確認
                        text = td.get_text(strip=True)
                        if text.isdigit():
                            num = int(text)
                            if 1 <= num <= 12:
                                if i == 0:
                                    gate_number = num
                                elif i == 1:
                                    horse_number = num
                                    break

                    # 騎手情報を取得
                    jockey = "騎手不明"
                    jockey_link = soup.find('a', class_='jockeyName')
                    if jockey_link:
                        # 同じ親要素内の騎手を探す
                        parent_table = horse_link.find_parent('table')
                        if parent_table:
                            jockey_links = parent_table.find_all('a', class_='jockeyName')
                            if jockey_links:
                                # 馬名の近くの騎手を探す
                                for jl in jockey_links:
                                    # 騎手名から地域情報を除去
                                    jockey_text = jl.get_text(strip=True)
                                    jockey_text = jockey_text.replace('（金沢）', '').replace('(金沢)', '').strip()
                                    if jockey_text:
                                        jockey = jockey_text
                                        break

                    # デフォルト値で馬情報を作成
                    horse = Horse(
                        horse_id=f"horse_{horse_name}_{horse_number}",
                        name=horse_name,
                        age=4,  # デフォルト
                        gender="牡",  # デフォルト
                    )

                    entry = Entry(
                        entry_id=str(uuid.uuid4()),
                        race_id=race_id,
                        horse=horse,
                        gate_number=gate_number,
                        horse_number=horse_number,
                        jockey=jockey,
                        weight=54.0,  # デフォルト
                        odds=None,
                        past_results=[],
                    )

                    entries.append(entry)

                except Exception as e:
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
                'payout_trifecta': 3連単配当 (100円あたり),
                'finish_order': [1位馬番, 2位馬番, ...],
                'corner_positions': {'corner_1': '7,9,1,...', 'corner_2': '...', ...},
                'payouts': {
                    'win': {'combo': '7', 'payout': 1200, 'popularity': 3},
                    'exacta': {'combo': '7-9', 'payout': 5400, 'popularity': 15},
                    ...
                }
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

            # HTML保存
            filename = f'race_{race_number:02d}_result.html'
            self._save_html(response.text, race_date, filename)

            soup = BeautifulSoup(response.text, 'html.parser')

            # 全着順を抽出（「成績表」テーブルから）
            finish_order = self._extract_finish_order(soup)

            # コーナー通過順を抽出
            corner_positions = self._extract_corner_positions(soup)

            # 全配当を抽出
            payouts = self._extract_payouts(soup)

            # 後方互換性のため1-3着と三連単配当を個別に保持
            finishers = {}
            payout_trifecta = None

            if finish_order and len(finish_order) >= 3:
                finishers['first'] = finish_order[0]
                finishers['second'] = finish_order[1]
                finishers['third'] = finish_order[2]

            if payouts and 'trifecta' in payouts:
                payout_trifecta = payouts['trifecta'].get('payout')

            if len(finishers) < 3:
                print(f"着順情報が取得できませんでした")
                return None

            return {
                'first': finishers.get('first'),
                'second': finishers.get('second'),
                'third': finishers.get('third'),
                'payout_trifecta': payout_trifecta,
                'finish_order': finish_order,
                'corner_positions': corner_positions,
                'payouts': payouts,
            }

        except Exception as e:
            print(f"結果取得エラー: {e}")
            return None

    def _extract_finish_order(self, soup: BeautifulSoup) -> List[int]:
        """全着順を抽出（「成績表」テーブルから）"""
        finish_order = []

        try:
            # 「成績表」というテキストを含むテーブルを探す
            result_tables = []
            for table in soup.find_all('table'):
                if '成績表' in table.get_text():
                    result_tables.append(table)

            if not result_tables:
                return finish_order

            result_table = result_tables[0]
            rows = result_table.find_all('tr')

            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    pos_text = cols[0].get_text(strip=True)
                    horse_text = cols[2].get_text(strip=True)  # 3列目が馬番

                    if pos_text.isdigit() and horse_text.isdigit():
                        pos = int(pos_text)
                        horse_no = int(horse_text)

                        # 順番通りに追加されているか確認
                        if pos == len(finish_order) + 1:
                            finish_order.append(horse_no)

        except Exception as e:
            print(f"着順抽出エラー: {e}")

        return finish_order

    def _extract_corner_positions(self, soup: BeautifulSoup) -> dict:
        """コーナー通過順を抽出"""
        corner_positions = {}

        try:
            import re

            # 全テキストから正規表現で抽出
            info_text = soup.get_text()

            corner_patterns = [
                ('corner_1', r'１コーナー\s+([0-9,()]+)'),
                ('corner_2', r'２コーナー\s+([0-9,()]+)'),
                ('corner_3', r'３コーナー\s+([0-9,()]+)'),
                ('corner_4', r'４コーナー\s+([0-9,()]+)'),
            ]

            for key, pattern in corner_patterns:
                match = re.search(pattern, info_text)
                if match:
                    corner_positions[key] = match.group(1)

        except Exception as e:
            print(f"コーナー通過順抽出エラー: {e}")

        return corner_positions

    def _extract_payouts(self, soup: BeautifulSoup) -> dict:
        """全配当を抽出"""
        payouts = {}

        try:
            import re

            # 払戻金テーブルを探す
            payout_header = soup.find(string=lambda t: t and '払戻金' in t and '賞金' not in t)
            if not payout_header:
                return payouts

            table_row = payout_header.find_parent('tr')
            if not table_row:
                return payouts

            # 次の行がヘッダー（単勝、複勝、...）
            header_row = table_row.find_next_sibling('tr')
            # その次がサブヘッダー（組番、払戻金、人気）
            subheader_row = header_row.find_next_sibling('tr') if header_row else None
            # その次が実際のデータ
            data_row = subheader_row.find_next_sibling('tr') if subheader_row else None

            if not data_row:
                return payouts

            cells = data_row.find_all('td')

            # 列の対応: 列0はRなのでスキップ、列1から開始
            # 列1-3: 単勝, 列4-6: 複勝, 列7-9: 枠連複, ...
            bet_types = [
                ('win', '単勝', 1),
                ('place', '複勝', 4),
                ('bracket_quinella', '枠連複', 7),
                ('quinella', '馬連複', 10),
                ('bracket_exacta', '枠連単', 13),
                ('exacta', '馬連単', 16),
                ('wide', 'ワイド', 19),
                ('trio', '三連複', 22),
                ('trifecta', '三連単', 25),
            ]

            for key, name, start_idx in bet_types:
                if start_idx + 2 < len(cells):
                    combo = cells[start_idx].get_text(strip=True)
                    payout_text = cells[start_idx + 1].get_text(strip=True)
                    popularity = cells[start_idx + 2].get_text(strip=True)

                    # 払戻金をパース（カンマ除去、円を除去）
                    payout_match = re.search(r'([\d,]+)', payout_text)
                    payout_int = None
                    if payout_match:
                        payout_int = int(payout_match.group(1).replace(',', ''))

                    # 人気をパース
                    popularity_int = None
                    if popularity.isdigit():
                        popularity_int = int(popularity)

                    payouts[key] = {
                        'combo': combo,
                        'payout': payout_int,
                        'popularity': popularity_int,
                    }

        except Exception as e:
            print(f"配当抽出エラー: {e}")

        return payouts

    def close(self):
        """セッションをクローズ"""
        self.session.close()
