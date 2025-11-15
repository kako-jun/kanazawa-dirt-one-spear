#!/usr/bin/env python3
"""
既存HTMLをYAML形式に変換
保存済みのHTMLファイルをパースしてYAML中間ファイルを生成
"""

import sys
import re
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parent))

# NARScraperのパース処理を流用するため、同じロジックをここに実装


def parse_html_file(html_path: Path, file_type: str) -> Optional[Dict]:
    """
    HTMLファイルをパースしてデータを抽出

    Args:
        html_path: HTMLファイルパス
        file_type: 'deba' または 'result'

    Returns:
        パースしたデータ辞書
    """
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        # ファイル名から日付とレース番号を抽出
        # 例: race_01_deba.html, race_12_result.html
        filename = html_path.stem
        parts = filename.split('_')
        race_number = int(parts[1]) if len(parts) > 1 else 0

        # 親ディレクトリ名から日付を取得
        # 例: data/html/2025/20250406/race_01_deba.html → 20250406
        date_str = html_path.parent.name
        race_date = datetime.strptime(date_str, '%Y%m%d')

        if file_type == 'deba':
            return _parse_deba(soup, race_date, race_number, html_path)
        elif file_type == 'result':
            return _parse_result(soup, race_date, race_number, html_path)
        else:
            return None

    except Exception as e:
        print(f"⚠️ {html_path.name} のパース失敗: {e}")
        return None


def _parse_deba(soup: BeautifulSoup, race_date: datetime, race_number: int, html_path: Path) -> Dict:
    """出馬表HTMLをパース（全データ取得版）"""

    # レース名を抽出
    title = soup.find('h2') or soup.find('h3')
    race_name = title.get_text(strip=True) if title else f"第{race_number}レース"

    # サブタイトル抽出 (準重賞などの格付け)
    subtitle = None
    subtitle_elem = soup.find('p', class_='subTitle')
    if subtitle_elem:
        subtitle = subtitle_elem.get_text(strip=True)

    # テキスト全体から情報を抽出
    info_text = soup.get_text()

    # 距離と周回方向
    distance = 1500
    direction = None

    distance_match = re.search(r'ダート\s*(\d{4})ｍ\s*（(左|右)）', info_text)
    if distance_match:
        distance = int(distance_match.group(1))
        direction = distance_match.group(2) + '回り'
    else:
        distance_match2 = re.search(r'(\d{4})m|ダ(\d{4})', info_text)
        if distance_match2:
            distance = int(distance_match2.group(1) or distance_match2.group(2))

    # 馬場状態
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

    # 賞金を抽出 (例: "賞金　1着450,000円　2着144,000円　...")
    prize_money = {}
    prize_match = re.search(r'賞金\s+(.+?)(?:\s|$)', info_text)
    if prize_match:
        prize_text = prize_match.group(1)
        # "1着450,000円　2着144,000円..." のパターンをパース
        for place_match in re.finditer(r'(\d+)着([\d,]+)円', prize_text):
            place = int(place_match.group(1))
            amount = int(place_match.group(2).replace(',', ''))
            prize_money[f'{place}着'] = amount

    # レース条件を抽出 (例: "サラブレッド系　一般 定量")
    race_class = None  # サラブレッド系 / アングロアラブ系
    race_category = None  # 一般 / 牝馬限定 / 若駒
    weight_system = None  # 定量 / 別定 / ハンデ

    race_condition_match = re.search(r'(サラブレッド系|アングロアラブ系)\s+(一般|牝馬限定|若駒|牝)\s+(定量|別定|ハンデ)', info_text)
    if race_condition_match:
        race_class = race_condition_match.group(1)
        race_category = race_condition_match.group(2)
        weight_system = race_condition_match.group(3)

    # 電話投票コードを抽出 (例: "41#")
    betting_code = None
    betting_code_match = re.search(r'電話投票コード[：:]\s*(\d+#)', info_text)
    if betting_code_match:
        betting_code = betting_code_match.group(1)

    # 出走馬情報を詳細に抽出
    horses = []
    horse_links = soup.find_all('a', class_='horseName')

    for idx, horse_link in enumerate(horse_links):
        try:
            horse_name = horse_link.get_text(strip=True)
            if not horse_name:
                continue

            # 馬名のある行から5行分のデータを取得
            # 構造: 1行目=馬名・騎手・オッズ・着別成績
            #       2行目=性齢・毛色・生年月日・今回斤量・過去レース名
            #       3行目=父馬・調教師・馬体重・過去5走の詳細(人気・体重・騎手・斤量)
            #       4行目=母馬・生産者・空白・過去5走の詳細(タイム・コーナー・上り)
            #       5行目=母父・空白・空白・過去5走の詳細(着差・1着馬)

            horse_row = horse_link.find_parent('tr')
            if not horse_row:
                continue

            # 枠番・馬番を取得（rowspan=5のセルから）
            gate_number = None
            horse_number = None

            for td in horse_row.find_all('td', class_='courseNum'):
                text = td.get_text(strip=True)
                if text.isdigit():
                    gate_number = int(text)
                    break

            for td in horse_row.find_all('td', class_='horseNum'):
                text = td.get_text(strip=True)
                if text.isdigit():
                    horse_number = int(text)
                    break

            if not horse_number:
                horse_number = idx + 1
            if not gate_number:
                gate_number = 1

            # 騎手情報（同じ行から）
            jockey = "不明"
            jockey_link = horse_row.find('a', class_='jockeyName')
            if jockey_link:
                jockey = jockey_link.get_text(strip=True).replace('（金沢）', '').replace('(金沢)', '').strip()

            # 次の行（2行目）から性齢・毛色・生年月日・斤量・着別成績を取得
            next_row = horse_row.find_next_sibling('tr')
            sex_age = None
            coat_color = None
            birth_date = None
            weight_carried = None
            career_record = None

            if next_row:
                cells = next_row.find_all('td')
                if len(cells) >= 4:
                    # 性齢（例: "牝6"）
                    sex_age_elem = cells[0].find('span', class_='male')
                    if sex_age_elem:
                        sex_age = sex_age_elem.get_text(strip=True)

                    # 毛色
                    if len(cells) > 1:
                        coat_color = cells[1].get_text(strip=True)

                    # 生年月日
                    if len(cells) > 2:
                        birth_date = cells[2].get_text(strip=True)

                    # 斤量と着別成績（例: "55.0　0-1-2-22"）
                    if len(cells) > 3:
                        weight_record = cells[3].get_text(strip=True)
                        parts = weight_record.split('　')
                        if len(parts) >= 1:
                            try:
                                weight_carried = float(parts[0])
                            except:
                                pass
                        if len(parts) >= 2:
                            career_record = parts[1]

            # 3行目から父馬・調教師・馬体重を取得
            third_row = next_row.find_next_sibling('tr') if next_row else None
            sire = None
            trainer = None
            horse_weight = None
            weight_diff = None

            if third_row:
                cells = third_row.find_all('td')
                # 父馬（最初の3列結合セル）
                if len(cells) > 0:
                    sire = cells[0].get_text(strip=True)

                # 調教師（リンクがある）
                trainer_link = third_row.find('a', href=re.compile('TrainerMark'))
                if trainer_link:
                    trainer = trainer_link.get_text(strip=True).replace('（金沢）', '').strip()

                # 馬体重・増減（rowspan=2のodds_weightクラス）
                weight_cell = third_row.find('td', class_='odds_weight')
                if weight_cell:
                    weight_text = weight_cell.get_text(strip=True)
                    # 例: "443(+4)" or "443<br>(+4)"
                    weight_match = re.search(r'(\d+)', weight_text)
                    diff_match = re.search(r'\(([+-]\d+)\)', weight_text)
                    if weight_match:
                        try:
                            horse_weight = int(weight_match.group(1))
                        except:
                            pass
                    if diff_match:
                        weight_diff = diff_match.group(1)

            # 4行目・5行目から母馬・母父・生産者を取得
            dam = None  # 母馬
            broodmare_sire = None  # 母父
            breeder = None  # 生産者

            fourth_row = third_row.find_next_sibling('tr') if third_row else None
            if fourth_row:
                cells = fourth_row.find_all('td')
                # 母馬（colspan=3の最初のセル）
                if len(cells) > 0:
                    dam = cells[0].get_text(strip=True)
                # 生産者（2番目のセル）
                if len(cells) > 1:
                    breeder = cells[1].get_text(strip=True)

            fifth_row = fourth_row.find_next_sibling('tr') if fourth_row else None
            if fifth_row:
                cells = fifth_row.find_all('td')
                # 母父（括弧書きで表示: "（ディープインパクト）"）
                if len(cells) > 0:
                    text = cells[0].get_text(strip=True)
                    # 括弧を除去
                    broodmare_sire = text.replace('（', '').replace('）', '').replace('(', '').replace(')', '')

            # 着別成績詳細と最高タイムを取得
            # rowspan=5のセル内にある table.arrival から
            detailed_record = None
            best_time = None
            best_time_good_track = None

            arrival_table = horse_row.find('table', class_='arrival') if horse_row else None
            if arrival_table:
                try:
                    rows = arrival_table.find_all('tr')
                    if len(rows) >= 6:
                        # 各行から着別成績を取得 (1-2-3-4列目が成績)
                        def parse_record_row(row):
                            cells = row.find_all('td')
                            if len(cells) >= 5:
                                return {
                                    'wins': cells[1].get_text(strip=True).replace('-', ''),
                                    'places': cells[2].get_text(strip=True).replace('-', ''),
                                    'shows': cells[3].get_text(strip=True).replace('-', ''),
                                    'starts': cells[4].get_text(strip=True)
                                }
                            return None

                        detailed_record = {
                            'all': parse_record_row(rows[0]),  # 全
                            'left': parse_record_row(rows[1]),  # 左
                            'right': parse_record_row(rows[2]),  # 右
                            'venue': parse_record_row(rows[3]),  # 場
                            'distance': parse_record_row(rows[4]),  # 距
                        }

                        # 最終行から最高タイムを取得
                        if len(rows) >= 6:
                            time_cells = rows[5].find_all('td')
                            if len(time_cells) >= 1:
                                best_time = time_cells[0].get_text(strip=True)
                            if len(time_cells) >= 2:
                                best_time_good_track = time_cells[1].get_text(strip=True)
                except Exception as e:
                    # 着別成績抽出エラーは無視
                    pass

            # 過去5走のデータを取得
            # HTML構造:
            # - 2行目の5-9列目: レース名
            # - 3行目の5-9列目: 人気、馬体重、騎手、斤量
            # - 4行目の5-9列目: タイム、コーナー通過順、上り3F
            # - 5行目の5-9列目: 着差、1着馬
            # - 1行目（horse_row）の過去走情報セル: 着順、日付、馬場、頭数、場所・距離・馬番
            past_races = []

            # 1行目から過去走の基本情報を取得
            # 構造: <td><div class="raceInfo">...</div></td>
            race_info_divs = horse_row.find_all('div', class_='raceInfo') if horse_row else []

            for race_idx in range(min(5, len(race_info_divs))):
                try:
                    race_info_div = race_info_divs[race_idx]
                    race_text = race_info_div.get_text(separator=' ', strip=True)

                    # 着順（span.pastRank）
                    rank_elem = race_info_div.find('span', class_='pastRank')
                    rank = rank_elem.get_text(strip=True) if rank_elem else None

                    # 日付・馬場・頭数・場所の抽出
                    # 例: "25.03.24　良　5頭 金沢　右1400　2番"
                    date_match = re.search(r'(\d{2}\.\d{2}\.\d{2})', race_text)
                    track_match = re.search(r'(良|稍重|重|不良)', race_text)
                    heads_match = re.search(r'(\d+)頭', race_text)
                    course_match = re.search(r'(金沢|笠松|名古屋|園田|佐賀|高知|川崎)\s+(左|右)?(\d+)\s+(\d+)番', race_text)

                    race_data = {
                        'rank': rank,
                        'date': date_match.group(1) if date_match else None,
                        'track_condition': track_match.group(1) if track_match else None,
                        'num_horses': int(heads_match.group(1)) if heads_match else None,
                    }

                    if course_match:
                        race_data['venue'] = course_match.group(1)
                        race_data['direction'] = course_match.group(2)
                        race_data['distance'] = int(course_match.group(3))
                        race_data['post_position'] = int(course_match.group(4))

                    # 2行目からレース名
                    if next_row:
                        race_link_cells = next_row.find_all('a', class_='race')
                        if race_idx < len(race_link_cells):
                            race_data['race_name'] = race_link_cells[race_idx].get_text(strip=True)

                    # 3行目から人気・馬体重・騎手・斤量
                    if third_row:
                        third_cells = third_row.find_all('td', class_='')
                        # 3行目の該当セル（通常4列目以降）
                        offset_idx = race_idx
                        if offset_idx < len(third_cells):
                            cell_text = third_cells[offset_idx].get_text(strip=True)
                            # 例: "5人　439　甲賀弘 54.0"
                            pop_match = re.search(r'(\d+)人', cell_text)
                            weight_match = re.search(r'(\d+)\s+', cell_text)
                            jockey_match = re.search(r'(\S+)\s+([\d.]+)$', cell_text)

                            if pop_match:
                                race_data['popularity'] = int(pop_match.group(1))
                            if weight_match:
                                race_data['horse_weight'] = int(weight_match.group(1))
                            if jockey_match:
                                race_data['past_jockey'] = jockey_match.group(1)
                                race_data['past_weight_carried'] = float(jockey_match.group(2))

                    # 4行目からタイム・コーナー・上り3F
                    if fourth_row:
                        fourth_cells = fourth_row.find_all('td', class_='')
                        offset_idx = race_idx
                        if offset_idx < len(fourth_cells):
                            cell_text = fourth_cells[offset_idx].get_text(strip=True)
                            # 例: "1:33.2　5-5-4-4　39.9"
                            time_match = re.search(r'([\d:]+\.?\d*)', cell_text)
                            corner_match = re.search(r'([\d-]+)', cell_text)
                            last3f_match = re.search(r'([\d.]+)$', cell_text)

                            if time_match:
                                race_data['time'] = time_match.group(1)
                            if corner_match:
                                race_data['corner_positions'] = corner_match.group(1)
                            if last3f_match:
                                race_data['last_3f'] = last3f_match.group(1)

                    # 5行目から着差・1着馬
                    if fifth_row:
                        fifth_cells = fifth_row.find_all('td', class_='')
                        offset_idx = race_idx
                        if offset_idx < len(fifth_cells):
                            cell_text = fifth_cells[offset_idx].get_text(strip=True)
                            # 例: "1.7　デイドリームビーチ"
                            margin_match = re.search(r'^([\d.]+)', cell_text)
                            winner_match = re.search(r'\s+(\S+)$', cell_text)

                            if margin_match:
                                race_data['margin'] = margin_match.group(1)
                            if winner_match:
                                race_data['winner'] = winner_match.group(1)

                    past_races.append(race_data)

                except Exception as e:
                    # 個別の過去走データ抽出エラーは無視して続行
                    pass

            horses.append({
                'horse_number': horse_number,
                'gate_number': gate_number,
                'horse_name': horse_name,
                'sex_age': sex_age,
                'coat_color': coat_color,
                'birth_date': birth_date,
                'jockey': jockey,
                'trainer': trainer,
                'weight_carried': weight_carried,
                'career_record': career_record,  # 例: "0-1-2-22"
                'sire': sire,  # 父馬
                'dam': dam,  # 母馬
                'broodmare_sire': broodmare_sire,  # 母父
                'breeder': breeder,  # 生産者
                'horse_weight': horse_weight,
                'weight_diff': weight_diff,
                'detailed_record': detailed_record,  # 着別成績詳細
                'best_time': best_time,  # 最高タイム
                'best_time_good_track': best_time_good_track,  # 良馬場最高タイム
                'past_races': past_races if past_races else None,  # 過去5走の詳細
                'odds': None,  # オッズは別途取得が必要
            })

        except Exception as e:
            print(f"馬情報抽出エラー: {e}")
            import traceback
            traceback.print_exc()
            continue

    race_id = f"{race_date.strftime('%Y%m%d')}_{race_number:02d}"

    return {
        'meta': {
            'source_file': html_path.name,
            'extracted_at': datetime.now().isoformat(),
            'race_type': 'deba',
        },
        'race': {
            'race_id': race_id,
            'date': race_date.strftime('%Y-%m-%d'),
            'race_number': race_number,
            'name': race_name,
            'subtitle': subtitle,  # サブタイトル (準重賞など)
            'distance': distance,
            'track_condition': track_condition,
            'weather': weather,
            'direction': direction,
            'prize_money': prize_money if prize_money else None,
            'race_class': race_class,  # サラブレッド系 / アングロアラブ系
            'race_category': race_category,  # 一般 / 牝馬限定 / 若駒
            'weight_system': weight_system,  # 定量 / 別定 / ハンデ
            'betting_code': betting_code,  # 電話投票コード
        },
        'horses': horses,
    }


def _extract_horse_pedigree_info(soup: BeautifulSoup, horse_name: str) -> Dict:
    """
    レース結果HTMLから特定の馬の血統情報と生年月日を抽出

    HTML構造:
    <tr><td>馬名</td><td rowspan=4>馬名データ</td><td rowspan=2>父</td><td rowspan=2>父馬名</td><td>父</td><td colspan=3>父の父</td></tr>
    <tr><td>母</td><td colspan=3>父の母</td></tr>
    <tr><td rowspan=2>母</td><td rowspan=2>母馬名</td><td>父</td><td colspan=3>母の父</td></tr>
    <tr><td>母</td><td colspan=3>母の母</td></tr>
    <tr><td>調教師</td><td>...</td><td>生年月日</td><td>2013年3月18日</td><td>生産牧場</td><td>...</td></tr>
    <tr><td>馬主</td><td colspan=3>...</td><td>産地</td><td>...</td></tr>

    Args:
        soup: BeautifulSoup object
        horse_name: 馬名

    Returns:
        血統情報と生年月日の辞書
    """
    pedigree_info = {}

    try:
        # 「馬　情　報」を含む<td class="dbtitle">を探す
        # 複数見つかった場合は、行数が最も少ない（= 最もネストされた）テーブルを使用
        horse_info_tables = []
        for table in soup.find_all('table'):
            # class="dbtitle"のセルで「馬　情　報」を含むものを探す
            title_cells = table.find_all('td', class_='dbtitle')
            for cell in title_cells:
                if '馬　情　報' in cell.get_text():
                    rows = table.find_all('tr')
                    # 行数が10行以下の実際の馬情報テーブルのみを対象
                    if len(rows) <= 10:
                        horse_info_tables.append((table, len(rows)))
                    break

        # 行数が最も少ないテーブルを優先（最もネストされたテーブル = 実際のデータテーブル）
        horse_info_tables.sort(key=lambda x: x[1])

        # 該当する馬名のテーブルを見つける
        for table, row_count in horse_info_tables:
            table_text = table.get_text()
            if horse_name not in table_text:
                continue

            # 馬名が含まれるテーブルが見つかった
            rows = table.find_all('tr')

            sire = None  # 父
            dam = None  # 母
            sire_of_sire = None  # 父の父
            dam_of_sire = None  # 父の母
            sire_of_dam = None  # 母の父
            dam_of_dam = None  # 母の母
            birth_date = None  # 生年月日
            farm = None  # 生産牧場
            birthplace = None  # 産地

            # テーブル構造に基づいて直接抽出
            # 行1: 父、父の父
            # 行2: 父の母
            # 行3: 母、母の父
            # 行4: 母の母
            # 行5: 調教師、生年月日、生産牧場
            # 行6: 馬主、産地

            pedigree_rows = []
            for row in rows:
                if row.find('td', string=lambda t: t and '馬　情　報' in t):
                    # ヘッダー行なのでスキップ
                    continue
                pedigree_rows.append(row)

            if len(pedigree_rows) >= 6:
                # 行1 (index 0): 父と父の父
                row1_cells = pedigree_rows[0].find_all('td')
                # <td>馬名</td><td rowspan=4>馬名</td><td rowspan=2>父</td><td rowspan=2>父馬名</td><td>父</td><td colspan=3>父の父</td>
                if len(row1_cells) >= 6:
                    sire = row1_cells[3].get_text(strip=True)
                    sire_of_sire = row1_cells[5].get_text(strip=True)

                # 行2 (index 1): 父の母
                row2_cells = pedigree_rows[1].find_all('td')
                # <td>母</td><td colspan=3>父の母</td>
                if len(row2_cells) >= 2:
                    dam_of_sire = row2_cells[1].get_text(strip=True)

                # 行3 (index 2): 母と母の父
                row3_cells = pedigree_rows[2].find_all('td')
                # <td rowspan=2>母</td><td rowspan=2>母馬名</td><td>父</td><td colspan=3>母の父</td>
                if len(row3_cells) >= 4:
                    dam = row3_cells[1].get_text(strip=True)
                    sire_of_dam = row3_cells[3].get_text(strip=True)

                # 行4 (index 3): 母の母
                row4_cells = pedigree_rows[3].find_all('td')
                # <td>母</td><td colspan=3>母の母</td>
                if len(row4_cells) >= 2:
                    dam_of_dam = row4_cells[1].get_text(strip=True)

                # 行5 (index 4): 生年月日と生産牧場
                row5_cells = pedigree_rows[4].find_all('td')
                # <td>調教師</td><td>...</td><td>生年月日</td><td>2013年3月18日</td><td>生産牧場</td><td>...</td>
                for i, cell in enumerate(row5_cells):
                    cell_text = cell.get_text(strip=True)
                    if cell_text == '生年月日' and i + 1 < len(row5_cells):
                        birth_date_text = row5_cells[i + 1].get_text(strip=True)
                        # 「2013年3月18日」形式を「2013-03-18」に変換
                        match = re.match(r'(\d{4})年(\d{1,2})月(\d{1,2})日', birth_date_text)
                        if match:
                            year, month, day = match.groups()
                            birth_date = f"{year}-{int(month):02d}-{int(day):02d}"
                    if cell_text == '生産牧場' and i + 1 < len(row5_cells):
                        farm = row5_cells[i + 1].get_text(strip=True)

                # 行6 (index 5): 産地
                row6_cells = pedigree_rows[5].find_all('td')
                # <td>馬主</td><td colspan=3>...</td><td>産地</td><td>...</td>
                for i, cell in enumerate(row6_cells):
                    cell_text = cell.get_text(strip=True)
                    if cell_text == '産地' and i + 1 < len(row6_cells):
                        birthplace = row6_cells[i + 1].get_text(strip=True)

            # データをまとめる
            pedigree_info = {
                'sire': sire,
                'dam': dam,
                'sire_of_sire': sire_of_sire,
                'dam_of_sire': dam_of_sire,
                'sire_of_dam': sire_of_dam,
                'dam_of_dam': dam_of_dam,
                'birth_date': birth_date,
                'farm': farm,
                'birthplace': birthplace,
            }
            break

    except Exception as e:
        print(f"血統情報抽出エラー ({horse_name}): {e}")

    return pedigree_info


def _parse_result(soup: BeautifulSoup, race_date: datetime, race_number: int, html_path: Path) -> Dict:
    """結果HTMLをパース（NARScraperのロジックを流用）"""

    # 着順情報を抽出（「成績表」テーブルから全データ取得）
    finish_order = []
    result_details = []  # 各馬の詳細情報

    try:
        # 「成績表」というテキストを含むテーブルを探す
        result_tables = []
        for table in soup.find_all('table'):
            if '成績表' in table.get_text():
                result_tables.append(table)

        if result_tables:
            result_table = result_tables[0]
            rows = result_table.find_all('tr')

            for row in rows:
                cols = row.find_all('td')
                # 成績表の列構成: 着順、枠番、馬番、馬名、所属、性齢、負担重量、騎手、調教師、馬体重、差、タイム、着差、上り3F、人気
                if len(cols) >= 15:
                    pos_text = cols[0].get_text(strip=True)
                    horse_no_text = cols[2].get_text(strip=True)  # 3列目が馬番

                    if pos_text.isdigit() and horse_no_text.isdigit():
                        pos = int(pos_text)
                        horse_no = int(horse_no_text)

                        # 順番通りに追加されているか確認
                        if pos == len(finish_order) + 1:
                            finish_order.append(horse_no)

                            # 詳細情報を抽出
                            horse_name = cols[3].get_text(strip=True)  # 馬名
                            horse_detail = {
                                'finish_position': pos,
                                'gate_number': cols[1].get_text(strip=True),  # 枠番
                                'horse_number': horse_no,
                                'horse_name': horse_name,
                                'stable': cols[4].get_text(strip=True),  # 所属
                                'sex_age': cols[5].get_text(strip=True),  # 性齢
                                'weight_carried': cols[6].get_text(strip=True),  # 負担重量
                                'jockey': cols[7].get_text(strip=True),  # 騎手
                                'trainer': cols[8].get_text(strip=True),  # 調教師
                                'horse_weight': cols[9].get_text(strip=True),  # 馬体重
                                'weight_diff': cols[10].get_text(strip=True),  # 体重増減
                                'time': cols[11].get_text(strip=True),  # タイム
                                'margin': cols[12].get_text(strip=True),  # 着差
                                'last_3f': cols[13].get_text(strip=True),  # 上り3F
                                'popularity': cols[14].get_text(strip=True),  # 人気
                            }

                            # 血統情報と生年月日を抽出して追加
                            pedigree_info = _extract_horse_pedigree_info(soup, horse_name)
                            if pedigree_info:
                                horse_detail.update(pedigree_info)

                            result_details.append(horse_detail)

    except Exception as e:
        print(f"着順抽出エラー: {e}")

    # コーナー通過順を抽出
    corner_positions = {}

    try:
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

    # 上り4Fを抽出 (例: "上り 4F 51.3 3F 39.2")
    last_4f = None
    try:
        last_4f_match = re.search(r'上り\s+4F\s+([\d.]+)', info_text)
        if last_4f_match:
            last_4f = last_4f_match.group(1)
    except Exception as e:
        print(f"上り4F抽出エラー: {e}")

    # 馬場状態を抽出（正規表現で「馬場：」の直後を取得）
    track_condition = "不明"
    try:
        track_match = re.search(r'馬場[：:]\s*(不良|稍重|重|良)', info_text)
        if track_match:
            track_condition = track_match.group(1)
    except Exception as e:
        print(f"馬場状態抽出エラー: {e}")

    # 天候を抽出（正規表現で「天候：」の直後を取得）
    weather = "不明"
    try:
        weather_match = re.search(r'天候[：:]\s*(雪|雨|曇|晴)', info_text)
        if weather_match:
            weather = weather_match.group(1)
    except Exception as e:
        print(f"天候抽出エラー: {e}")

    # 全配当を抽出
    payouts = {}

    try:
        # 払戻金テーブルを探す
        payout_header = soup.find(string=lambda t: t and '払戻金' in t and '賞金' not in t)
        if payout_header:
            table_row = payout_header.find_parent('tr')
            if table_row:
                # 次の行がヘッダー（単勝、複勝、...）
                header_row = table_row.find_next_sibling('tr')
                # その次がサブヘッダー（組番、払戻金、人気）
                subheader_row = header_row.find_next_sibling('tr') if header_row else None
                # その次が実際のデータ
                data_row = subheader_row.find_next_sibling('tr') if subheader_row else None

                if data_row:
                    cells = data_row.find_all('td')

                    # 列の対応: 列0はRなのでスキップ、列1から開始
                    # 列1-3: 単勝, 列4-6: 複勝, 列7-9: 馬連複, ...
                    # 注: 枠連複・枠連単は金沢競馬では発売されていない
                    bet_types = [
                        ('win', '単勝', 1),
                        ('place', '複勝', 4),
                        ('quinella', '馬連複', 7),
                        ('exacta', '馬連単', 10),
                        ('wide', 'ワイド', 13),
                        ('trio', '三連複', 16),
                        ('trifecta', '三連単', 19),
                    ]

                    for key, name, start_idx in bet_types:
                        if start_idx + 2 < len(cells):
                            # <BR>タグで区切られた値を分割して最初の値を取得
                            combo_cell = cells[start_idx]
                            payout_cell = cells[start_idx + 1]
                            popularity_cell = cells[start_idx + 2]

                            # <BR>タグを改行に置き換えて分割
                            for br in combo_cell.find_all('br'):
                                br.replace_with('\n')
                            for br in payout_cell.find_all('br'):
                                br.replace_with('\n')
                            for br in popularity_cell.find_all('br'):
                                br.replace_with('\n')

                            combo_lines = combo_cell.get_text().strip().split('\n')
                            payout_lines = payout_cell.get_text().strip().split('\n')
                            popularity_lines = popularity_cell.get_text().strip().split('\n')

                            # 最初の値を取得
                            combo = combo_lines[0].strip() if combo_lines else ''
                            payout_text = payout_lines[0].strip() if payout_lines else ''
                            popularity = popularity_lines[0].strip() if popularity_lines else ''

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

    race_id = f"{race_date.strftime('%Y%m%d')}_{race_number:02d}"

    return {
        'meta': {
            'source_file': html_path.name,
            'extracted_at': datetime.now().isoformat(),
            'race_type': 'result',
        },
        'race_id': race_id,
        'track_condition': track_condition,  # 馬場状態
        'weather': weather,  # 天候
        'finish_order': finish_order,
        'result_details': result_details,  # 各馬の詳細情報
        'payouts': payouts,
        'corner_positions': corner_positions,
        'last_4f': last_4f,  # 上り4F
    }


def convert_directory(html_dir: Path, yaml_dir: Path, file_type: str = 'both'):
    """
    HTMLディレクトリを再帰的にスキャンしてYAML変換

    Args:
        html_dir: HTML格納ディレクトリ
        yaml_dir: YAML出力ディレクトリ
        file_type: 処理対象 ('deba', 'result', 'both')
    """
    yaml_dir.mkdir(parents=True, exist_ok=True)

    total_files = 0
    success_count = 0
    error_count = 0

    print(f"\n{'='*60}")
    print(f"HTML → YAML 変換開始")
    print(f"入力: {html_dir}")
    print(f"出力: {yaml_dir}")
    print(f"対象: {file_type}")
    print(f"{'='*60}\n")

    # HTMLファイルを再帰的に検索
    for html_file in sorted(html_dir.rglob('*.html')):
        # race_list.htmlはスキップ
        if 'race_list' in html_file.name:
            continue

        total_files += 1

        # ファイル種別を判定
        is_deba = '_deba.html' in html_file.name
        is_result = '_result.html' in html_file.name

        # 処理対象をフィルター
        if file_type == 'deba' and not is_deba:
            continue
        if file_type == 'result' and not is_result:
            continue

        # パース実行
        try:
            if is_deba:
                data = parse_html_file(html_file, 'deba')
            elif is_result:
                data = parse_html_file(html_file, 'result')
            else:
                continue

            if data is None:
                error_count += 1
                continue

            # YAML出力パスを決定（ディレクトリ構造を維持）
            relative_path = html_file.relative_to(html_dir)
            yaml_path = yaml_dir / relative_path.with_suffix('.yaml')
            yaml_path.parent.mkdir(parents=True, exist_ok=True)

            # YAML書き込み
            with open(yaml_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

            success_count += 1

            if success_count % 100 == 0:
                print(f"進捗: {success_count}/{total_files} 件処理完了")

        except Exception as e:
            print(f"❌ エラー ({html_file.name}): {e}")
            error_count += 1

    # 最終統計
    print(f"\n{'='*60}")
    print(f"変換完了")
    print(f"  総ファイル数: {total_files}")
    print(f"  成功: {success_count}")
    print(f"  失敗: {error_count}")
    print(f"  成功率: {success_count/total_files*100:.1f}%" if total_files > 0 else "  成功率: N/A")
    print(f"{'='*60}\n")


def main():
    """メイン処理"""
    import argparse

    parser = argparse.ArgumentParser(description='HTML → YAML 変換')
    parser.add_argument('html_dir', help='HTMLファイルのディレクトリ')
    parser.add_argument('--yaml-dir', default='data/yaml', help='YAML出力ディレクトリ（デフォルト: data/yaml）')
    parser.add_argument('--type', choices=['deba', 'result', 'both'], default='both',
                        help='処理対象タイプ（デフォルト: both）')

    args = parser.parse_args()

    html_dir = Path(args.html_dir)
    yaml_dir = Path(args.yaml_dir)

    if not html_dir.exists():
        print(f"❌ エラー: {html_dir} が存在しません")
        return 1

    convert_directory(html_dir, yaml_dir, args.type)
    return 0


if __name__ == '__main__':
    exit(main())
