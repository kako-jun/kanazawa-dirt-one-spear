#!/usr/bin/env python3
"""
YAML → DB インポートスクリプト（完全正規化版）
convert_html_to_yaml.pyで生成されたYAMLファイルを完全正規化されたDBにインポート

特徴:
- 騎手/調教師マスタの自動登録
- 血統馬の自動登録（自己参照FK）
- 名前の正規化（所属情報除去）
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import yaml
import re
from sqlalchemy.orm import Session
from app.database import (
    SessionLocal, DBRace, DBHorse, DBEntry, DBResult,
    DBJockey, DBTrainer, DBRacePerformance, DBPayout,
    engine, Base
)

# データベース初期化
Base.metadata.create_all(bind=engine)


def get_or_create_jockey(session: Session, jockey_name: str) -> str:
    """
    騎手マスタから取得、存在しなければ作成

    Args:
        session: DBセッション
        jockey_name: 騎手名（例: "中島龍(金沢)"）

    Returns:
        jockey_id
    """
    if not jockey_name:
        jockey_name = "不明"

    # 所属情報を除去して正規化名を作成
    normalized_name = re.sub(r'\([^)]*\)', '', jockey_name).strip()

    # 既存の騎手を検索
    jockey = session.query(DBJockey).filter_by(name=jockey_name).first()
    if jockey:
        return jockey.jockey_id

    # 新規作成
    jockey_id = f"jockey_{jockey_name}"
    jockey = DBJockey(
        jockey_id=jockey_id,
        name=jockey_name,
        name_normalized=normalized_name
    )
    session.add(jockey)
    return jockey_id


def get_or_create_trainer(session: Session, trainer_name: Optional[str]) -> Optional[str]:
    """
    調教師マスタから取得、存在しなければ作成

    Args:
        session: DBセッション
        trainer_name: 調教師名

    Returns:
        trainer_id (None可)
    """
    if not trainer_name:
        return None

    # 既存の調教師を検索
    trainer = session.query(DBTrainer).filter_by(name=trainer_name).first()
    if trainer:
        return trainer.trainer_id

    # 新規作成
    trainer_id = f"trainer_{trainer_name}"
    trainer = DBTrainer(
        trainer_id=trainer_id,
        name=trainer_name
    )
    session.add(trainer)
    return trainer_id


def get_or_create_horse(session: Session, horse_name: str, birth_date: Optional[str] = None,
                       is_runner: bool = False) -> str:
    """
    馬マスタから取得、存在しなければ作成

    Args:
        session: DBセッション
        horse_name: 馬名
        birth_date: 生年月日（例: "04.05生"）
        is_runner: 出走馬フラグ

    Returns:
        horse_id
    """
    if not horse_name:
        horse_name = "不明"

    # 馬IDの生成
    if birth_date:
        horse_id = f"{horse_name}_{birth_date}"
    else:
        horse_id = horse_name

    # 既存の馬を検索
    horse = session.query(DBHorse).filter_by(horse_id=horse_id).first()
    if horse:
        # 出走馬フラグを更新
        if is_runner and not horse.is_runner:
            horse.is_runner = True
        return horse.horse_id

    # 新規作成（血統情報はあとで設定）
    horse = DBHorse(
        horse_id=horse_id,
        name=horse_name,
        birth_date=birth_date,
        age=None,
        gender=None,
        is_runner=is_runner
    )
    session.add(horse)
    return horse_id


def import_deba_yaml(yaml_path: Path, session: Session) -> bool:
    """
    出馬表YAMLをDBにインポート（完全正規化版）

    Args:
        yaml_path: YAMLファイルのパス
        session: SQLAlchemyセッション

    Returns:
        成功ならTrue
    """
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        # YAMLファイルからrace_idを取得
        race_data = data.get('race', {})
        race_id = race_data.get('race_id')

        if not race_id:
            print(f"⚠️ race_id なし: {yaml_path.name}")
            return False

        # レースが既に存在するか確認
        existing_race = session.query(DBRace).filter_by(race_id=race_id).first()
        if existing_race:
            # 既存レースは更新しない
            return True

        # レース情報を登録
        race = DBRace(
            race_id=race_id,
            date=datetime.strptime(race_data.get('date', '2000-01-01'), '%Y-%m-%d'),
            race_number=race_data.get('race_number', 0),
            name=race_data.get('name', '不明'),
            subtitle=race_data.get('subtitle', None),
            distance=race_data.get('distance', 0),
            track_condition=race_data.get('track_condition', '良'),
            weather=race_data.get('weather', '晴'),
            direction=race_data.get('direction', None),
            prize_money=race_data.get('prize_money', None),
            race_class=race_data.get('race_class', None),
            race_category=race_data.get('race_category', None),
            weight_system=race_data.get('weight_system', None),
            betting_code=race_data.get('betting_code', None),
        )
        session.add(race)

        # 出走馬を登録
        horses_data = data.get('horses', [])
        for horse_data in horses_data:
            horse_name = horse_data.get('horse_name', '不明')
            birth_date = horse_data.get('birth_date', None)
            sex_age = horse_data.get('sex_age', None)
            age, gender = _parse_sex_age(sex_age)

            # 出走馬を登録
            horse_id = get_or_create_horse(session, horse_name, birth_date, is_runner=True)

            # 血統馬を先に登録（親馬もhorsesテーブルに）
            sire_name = horse_data.get('sire', None)
            dam_name = horse_data.get('dam', None)
            broodmare_sire_name = horse_data.get('broodmare_sire', None)

            sire_id = None
            dam_id = None
            broodmare_sire_id = None

            if sire_name:
                sire_id = get_or_create_horse(session, sire_name, is_runner=False)
            if dam_name:
                dam_id = get_or_create_horse(session, dam_name, is_runner=False)
            if broodmare_sire_name:
                broodmare_sire_id = get_or_create_horse(session, broodmare_sire_name, is_runner=False)

            # 血統馬を確定してからFKを設定
            session.flush()

            # 出走馬の詳細情報と血統FKを更新
            horse = session.query(DBHorse).filter_by(horse_id=horse_id).first()
            if horse:
                horse.age = age
                horse.gender = gender
                horse.coat_color = horse_data.get('coat_color', None)
                horse.breeder = horse_data.get('breeder', None)
                horse.sire_id = sire_id
                horse.dam_id = dam_id
                horse.broodmare_sire_id = broodmare_sire_id

            # 騎手・調教師をマスタに登録
            jockey_name = horse_data.get('jockey', '不明')
            trainer_name = horse_data.get('trainer', None)

            jockey_id = get_or_create_jockey(session, jockey_name)
            trainer_id = get_or_create_trainer(session, trainer_name)

            # マスタ登録を確定（UNIQUE制約違反を防ぐ）
            session.flush()

            # 出走情報を登録
            entry_id = f"{race_id}_{horse_data.get('horse_number', '0')}"

            entry = DBEntry(
                entry_id=entry_id,
                race_id=race_id,
                horse_id=horse_id,
                jockey_id=jockey_id,
                trainer_id=trainer_id,
                gate_number=_parse_int(horse_data.get('gate_number', '0')),
                horse_number=_parse_int(horse_data.get('horse_number', '0')),
                weight=_parse_float(horse_data.get('weight_carried', '0')) or 0.0,
                horse_weight=_parse_int(horse_data.get('horse_weight', None)),
                weight_diff=horse_data.get('weight_diff', None),
                career_record=horse_data.get('career_record', None),
                detailed_record=horse_data.get('detailed_record', None),
                best_time=horse_data.get('best_time', None),
                best_time_good_track=horse_data.get('best_time_good_track', None),
                odds=_parse_float(horse_data.get('odds', None)),
                past_results=horse_data.get('past_races', None),
            )
            session.add(entry)

        session.commit()
        return True

    except Exception as e:
        print(f"❌ {yaml_path.name} のインポート失敗: {e}")
        import traceback
        traceback.print_exc()
        session.rollback()
        return False


def import_result_yaml(yaml_path: Path, session: Session) -> bool:
    """
    結果YAMLをDBにインポート

    Args:
        yaml_path: YAMLファイルのパス
        session: SQLAlchemyセッション

    Returns:
        成功ならTrue
    """
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        # race_idを取得（トップレベルまたはrace.race_id）
        race_id = data.get('race_id')
        if not race_id:
            race_data = data.get('race', {})
            race_id = race_data.get('race_id')

        if not race_id:
            print(f"⚠️ race_id なし: {yaml_path.name}")
            return False

        # レース情報を取得（存在する場合）
        race_data = data.get('race', {})

        # 日付をrace_dataから取得、なければrace_idから抽出
        race_date_str = race_data.get('date')
        if not race_date_str and race_id:
            # race_idから日付を抽出（例: "20241124_01" → "2024-11-24"）
            try:
                date_part = race_id.split('_')[0]
                if len(date_part) == 8:
                    race_date_str = f"{date_part[0:4]}-{date_part[4:6]}-{date_part[6:8]}"
            except:
                pass
        if not race_date_str:
            race_date_str = '2000-01-01'

        # レースが存在するか確認
        race = session.query(DBRace).filter_by(race_id=race_id).first()
        if not race:
            print(f"⚠️ レースが未登録: {race_id}")
            # レースを先に作成（最低限の情報で）
            race = DBRace(
                race_id=race_id,
                date=datetime.strptime(race_date_str, '%Y-%m-%d'),
                race_number=race_data.get('race_number', 0),
                name=race_data.get('name', '不明（結果のみ）'),
                subtitle=race_data.get('subtitle', None),
                distance=race_data.get('distance', 0),
                track_condition=data.get('track_condition', race_data.get('track_condition', '不明')),
                weather=data.get('weather', race_data.get('weather', '不明')),
                direction=race_data.get('direction', None),
                prize_money=race_data.get('prize_money', None),
                race_class=race_data.get('race_class', None),
                race_category=race_data.get('race_category', None),
                weight_system=race_data.get('weight_system', None),
                betting_code=race_data.get('betting_code', None),
            )
            session.add(race)
        else:
            # 既存レースの馬場状態・天候を更新（トップレベルのデータがあれば）
            if 'track_condition' in data and data['track_condition'] != '不明':
                race.track_condition = data['track_condition']
            if 'weather' in data and data['weather'] != '不明':
                race.weather = data['weather']

        # 結果が既に存在するか確認
        existing_result = session.query(DBResult).filter_by(race_id=race_id).first()
        if existing_result:
            # 既存結果は更新
            session.delete(existing_result)

        # 着順情報を処理（トップレベルまたはresult以下）
        finish_order_data = data.get('finish_order', [])
        if not finish_order_data:
            result_data = data.get('result', {})
            finish_order_data = result_data.get('finish_order', [])

        # 馬番のリストとして抽出
        finish_order = []
        for item in finish_order_data:
            if isinstance(item, dict):
                horse_num = item.get('horse_number', 0)
            else:
                horse_num = item
            finish_order.append(int(horse_num) if horse_num else 0)

        # 上位3着を抽出
        first = finish_order[0] if len(finish_order) > 0 else None
        second = finish_order[1] if len(finish_order) > 1 else None
        third = finish_order[2] if len(finish_order) > 2 else None

        # 配当情報を処理（トップレベルまたはresult以下）
        payouts_data = data.get('payouts', {})
        if not payouts_data:
            payouts_data = data.get('result', {}).get('payouts', {})

        # 三連単配当を抽出
        trifecta_payout = None
        if 'trifecta' in payouts_data:
            trifecta = payouts_data.get('trifecta', {})
            trifecta_payout = _parse_payout_amount(trifecta.get('payout', 0))
        elif '3連単' in payouts_data:
            trifecta = payouts_data.get('3連単', {})
            trifecta_payout = _parse_payout_amount(trifecta.get('amount', '0'))
        elif '三連単' in payouts_data:
            trifecta = payouts_data.get('三連単', {})
            trifecta_payout = _parse_payout_amount(trifecta.get('amount', '0'))

        # コーナー通過順を処理（トップレベルまたはresult以下）
        corner_positions = data.get('corner_positions', {})
        if not corner_positions:
            corner_positions = data.get('result', {}).get('corner_positions', {})

        # 結果を登録（JSON型カラムを削除）
        result_id = f"result_{race_id}"

        result = DBResult(
            result_id=result_id,
            race_id=race_id,
            first=first,
            second=second,
            third=third,
            payout_trifecta=trifecta_payout,
            prediction_hit=False,
            purchased=False,
            bet_amount=0,
            return_amount=0,
            recorded_at=datetime.now(),
            memo=None,
        )
        session.add(result)

        # 配当情報を登録（payoutsテーブルに正規化）
        # 既存の配当データを削除
        session.query(DBPayout).filter_by(race_id=race_id).delete()

        # 配当データを登録
        payout_idx = 0
        for payout_type_key, payout_info in payouts_data.items():
            if isinstance(payout_info, dict):
                payout_id = f"{race_id}_{payout_type_key}_{payout_idx}"
                payout_obj = DBPayout(
                    payout_id=payout_id,
                    race_id=race_id,
                    payout_type=payout_type_key,
                    combo=str(payout_info.get('combo', '')),
                    payout=_parse_payout_amount(payout_info.get('payout', 0)),
                    popularity=_parse_int_safe(payout_info.get('popularity')),
                )
                session.add(payout_obj)
                payout_idx += 1

        # result_details内の馬情報を処理（race_performancesテーブルに投入）
        # 既存のパフォーマンスデータを削除
        session.query(DBRacePerformance).filter_by(race_id=race_id).delete()

        result_details_data = data.get('result_details', [])
        if result_details_data:
            for detail in result_details_data:
                try:
                    horse_name = detail.get('horse_name', None)
                    sex_age = detail.get('sex_age', None)
                    horse_number = detail.get('horse_number', None)
                    gate_number = detail.get('gate_number', None)
                    finish_position = detail.get('finish_position', None)
                    popularity = detail.get('popularity', None)
                    time = detail.get('time', None)
                    margin = detail.get('margin', None)
                    last_3f = detail.get('last_3f', None)

                    if not horse_name:
                        continue

                    # 性別・年齢をパース
                    age, gender = _parse_sex_age(sex_age) if sex_age else (None, None)

                    # このレースのエントリーから馬を特定
                    entry = None
                    horse = None
                    entry_id = None

                    if horse_number:
                        entry_id = f"{race_id}_{horse_number}"
                        entry = session.query(DBEntry).filter_by(entry_id=entry_id).first()
                        if entry:
                            horse = session.query(DBHorse).filter_by(horse_id=entry.horse_id).first()
                            if horse:
                                # 年齢・性別が未設定の場合のみ更新
                                if age and not horse.age:
                                    horse.age = age
                                if gender and not horse.gender:
                                    horse.gender = gender
                        else:
                            # エントリーがない場合は馬名で検索（フォールバック）
                            horse = session.query(DBHorse).filter_by(name=horse_name).first()
                            if horse and age and gender:
                                if age and not horse.age:
                                    horse.age = age
                                if gender and not horse.gender:
                                    horse.gender = gender
                    else:
                        # 馬番がない場合は馬名で検索
                        horse = session.query(DBHorse).filter_by(name=horse_name).first()
                        if horse and age and gender:
                            if age and not horse.age:
                                horse.age = age
                            if gender and not horse.gender:
                                horse.gender = gender

                    # race_performanceを登録
                    if horse and horse_number:
                        performance_id = f"{race_id}_{horse_number}_perf"

                        # corner_positions からこの馬のコーナー通過順を抽出
                        corner_1 = _extract_horse_corner_position(corner_positions.get('corner_1', ''), horse_number)
                        corner_2 = _extract_horse_corner_position(corner_positions.get('corner_2', ''), horse_number)
                        corner_3 = _extract_horse_corner_position(corner_positions.get('corner_3', ''), horse_number)
                        corner_4 = _extract_horse_corner_position(corner_positions.get('corner_4', ''), horse_number)

                        performance = DBRacePerformance(
                            performance_id=performance_id,
                            race_id=race_id,
                            entry_id=entry_id,
                            horse_id=horse.horse_id,
                            gate_number=_parse_int_safe(gate_number),
                            horse_number=_parse_int_safe(horse_number),
                            finish_position=_parse_int_safe(finish_position),
                            popularity=_parse_int_safe(popularity),
                            time=time,
                            margin=margin,
                            last_3f=last_3f,
                            last_4f=data.get('last_4f', None),  # レース全体の上がり4F
                            corner_1_position=corner_1,
                            corner_2_position=corner_2,
                            corner_3_position=corner_3,
                            corner_4_position=corner_4,
                        )
                        session.add(performance)

                except Exception as e:
                    # 個別のエラーはスキップ
                    print(f"⚠️ パフォーマンス登録エラー ({horse_name}): {e}")
                    continue

        session.commit()
        return True

    except Exception as e:
        print(f"❌ {yaml_path.name} のインポート失敗: {e}")
        import traceback
        traceback.print_exc()
        session.rollback()
        return False


def _parse_sex_age(sex_age_str: Optional[str]) -> tuple:
    """
    性別・年齢文字列をパース
    例: "牝6" → (6, "female")
    """
    if not sex_age_str:
        return None, None

    age_match = re.search(r'(\d+)', sex_age_str)
    age = int(age_match.group(1)) if age_match else None

    gender = None
    if '牡' in sex_age_str:
        gender = 'male'
    elif '牝' in sex_age_str:
        gender = 'female'
    elif 'セ' in sex_age_str:
        gender = 'gelding'

    return age, gender


def _parse_int(value: Any) -> Optional[int]:
    """安全な整数変換"""
    try:
        if value is None:
            return None
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            cleaned = value.replace('+', '').replace('-', '').strip()
            return int(cleaned) if cleaned else None
        return None
    except:
        return None


def _parse_float(value: Any) -> Optional[float]:
    """安全な浮動小数点変換"""
    try:
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            match = re.search(r'(\d+\.?\d*)', value)
            return float(match.group(1)) if match else None
        return None
    except:
        return None


def _parse_payout_amount(amount_str: Any) -> Optional[int]:
    """配当金額文字列を整数に変換"""
    try:
        if isinstance(amount_str, int):
            return amount_str
        if isinstance(amount_str, str):
            cleaned = amount_str.replace(',', '').replace('円', '').strip()
            return int(cleaned) if cleaned else None
        return None
    except:
        return None


# エイリアス
_parse_int_safe = _parse_int


def _extract_horse_corner_position(corner_str: str, horse_number: int) -> Optional[str]:
    """
    コーナー通過順テキストから特定馬番の位置情報を抽出

    Args:
        corner_str: コーナー通過順（例: "3,5,7,4,(1,9),8,6,2"）
        horse_number: 馬番

    Returns:
        位置情報（簡易的にコーナー通過順そのものを返す）
    """
    # TODO: より詳細な位置抽出ロジックを実装
    # 現状はコーナー通過順全体を保存
    return corner_str if corner_str else None


def process_yaml_directory(yaml_dir: Path, race_type: str = 'both'):
    """
    YAMLディレクトリを再帰的にスキャンしてDBにインポート

    Args:
        yaml_dir: YAML格納ディレクトリ
        race_type: 処理対象 ('deba', 'result', 'both')
    """
    if not yaml_dir.exists():
        print(f"❌ エラー: {yaml_dir} が存在しません")
        return

    total_files = 0
    success_count = 0
    error_count = 0

    print(f"\n{'='*60}")
    print(f"YAML → DB インポート開始（完全正規化版）")
    print(f"入力: {yaml_dir}")
    print(f"対象: {race_type}")
    print(f"{'='*60}\n")

    session = SessionLocal()

    try:
        # YAMLファイルを再帰的に検索
        yaml_files = sorted(yaml_dir.rglob('*.yaml'))

        # フィルタリング
        if race_type == 'deba':
            yaml_files = [f for f in yaml_files if '_deba.yaml' in f.name]
        elif race_type == 'result':
            yaml_files = [f for f in yaml_files if '_result.yaml' in f.name]

        total_files = len(yaml_files)
        print(f"対象ファイル数: {total_files} 件\n")

        for yaml_file in yaml_files:
            # ファイル種別を判定
            is_deba = '_deba.yaml' in yaml_file.name
            is_result = '_result.yaml' in yaml_file.name

            # インポート実行
            try:
                if is_deba:
                    success = import_deba_yaml(yaml_file, session)
                elif is_result:
                    success = import_result_yaml(yaml_file, session)
                else:
                    print(f"⚠️ スキップ（種別不明）: {yaml_file.name}")
                    continue

                if success:
                    success_count += 1
                else:
                    error_count += 1

                if success_count % 100 == 0:
                    print(f"進捗: {success_count}/{total_files} 件インポート完了")

            except Exception as e:
                print(f"❌ エラー ({yaml_file.name}): {e}")
                error_count += 1

    finally:
        session.close()

    # 最終統計
    print(f"\n{'='*60}")
    print(f"インポート完了")
    print(f"  総ファイル数: {total_files}")
    print(f"  成功: {success_count}")
    print(f"  失敗: {error_count}")
    print(f"  成功率: {success_count/total_files*100:.1f}%" if total_files > 0 else "  成功率: N/A")
    print(f"{'='*60}\n")


def main():
    """メイン処理"""
    import argparse

    parser = argparse.ArgumentParser(description='YAML → DB インポート（完全正規化版）')
    parser.add_argument('yaml_dir', help='YAMLファイルのディレクトリ')
    parser.add_argument('--type', choices=['deba', 'result', 'both'], default='both',
                        help='処理対象タイプ（デフォルト: both）')

    args = parser.parse_args()

    yaml_dir = Path(args.yaml_dir)

    process_yaml_directory(yaml_dir, args.type)
    return 0


if __name__ == '__main__':
    exit(main())
