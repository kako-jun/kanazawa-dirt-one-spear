"""
サンプルデータ生成
"""
import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models import Race, Entry, Horse, Prediction
from app.database import get_db, init_db
from app import crud
from app.predictor import generate_simple_prediction


def create_sample_horses() -> list[Horse]:
    """サンプル馬データ"""
    horse_names = [
        "カナザワノホシ", "ダートキング", "マエダトシイエ", "ヒャクマンゴク",
        "カガノクニ", "ホクリクノカゼ", "キンジョウノツバサ", "イシカワノユメ",
        "ノトハントウ", "カガヤキ", "テッポウマチ", "ケンロクエン"
    ]

    horses = []
    for i, name in enumerate(horse_names):
        horse = Horse(
            horse_id=f"horse_{i+1:03d}",
            name=name,
            age=3 + (i % 5),  # 3-7歳
            gender=["牡", "牝", "セン"][i % 3]
        )
        horses.append(horse)

    return horses


def create_sample_race(race_number: int, date: datetime, horses: list[Horse]) -> Race:
    """サンプルレース作成"""
    import random

    race_names = [
        "金沢ダービー", "ダートスプリント", "加賀特別", "白山賞",
        "金沢記念", "兼六園杯", "能登半島特別", "北陸ダービー"
    ]

    # ランダムに8-12頭選択
    num_horses = random.randint(8, min(12, len(horses)))
    selected_horses = random.sample(horses, num_horses)

    entries = []
    for i, horse in enumerate(selected_horses):
        entry = Entry(
            entry_id=str(uuid.uuid4()),
            race_id=f"race_{date.strftime('%Y%m%d')}_{race_number:02d}",
            horse=horse,
            gate_number=(i % 8) + 1,
            horse_number=i + 1,
            jockey=f"騎手{chr(65 + i % 26)}",
            weight=54.0 + (i % 5),
            odds=random.uniform(1.5, 50.0),
            past_results=[random.randint(1, 10) for _ in range(5)]
        )
        entries.append(entry)

    race = Race(
        race_id=f"race_{date.strftime('%Y%m%d')}_{race_number:02d}",
        date=date,
        race_number=race_number,
        name=race_names[race_number % len(race_names)],
        distance=random.choice([1400, 1500, 1700, 2000]),
        track_condition=random.choice(["良", "稍重", "重"]),
        weather=random.choice(["晴", "曇", "雨"]),
        entries=entries
    )

    return race


def initialize_sample_data():
    """サンプルデータを初期化"""
    init_db()

    db = next(get_db())

    try:
        # 既存データがあればスキップ
        existing_races = crud.get_races(db)
        if existing_races:
            print("既にデータが存在します")
            return

        print("サンプルデータを生成中...")

        # 馬データ作成
        horses = create_sample_horses()

        # 過去1週間分のレースを作成
        today = datetime.now()
        for days_ago in range(7, 0, -1):
            race_date = today - timedelta(days=days_ago)
            race_date = race_date.replace(hour=14, minute=0, second=0, microsecond=0)

            # 1日に3-5レース
            num_races = 4
            for race_num in range(1, num_races + 1):
                race_time = race_date + timedelta(minutes=30 * (race_num - 1))
                race = create_sample_race(race_num, race_time, horses)

                # レース登録
                db_race = crud.create_race(db, race)
                print(f"作成: {race.date.strftime('%Y-%m-%d')} {race.name}")

                # 予想生成
                prediction = generate_simple_prediction(race)
                crud.create_prediction(db, prediction)

        # 未来のレース（今日と明日）も作成
        for days_ahead in range(0, 2):
            race_date = today + timedelta(days=days_ahead)
            race_date = race_date.replace(hour=14, minute=0, second=0, microsecond=0)

            num_races = 5
            for race_num in range(1, num_races + 1):
                race_time = race_date + timedelta(minutes=30 * (race_num - 1))
                race = create_sample_race(race_num, race_time, horses)

                db_race = crud.create_race(db, race)
                print(f"作成: {race.date.strftime('%Y-%m-%d')} {race.name}")

                # 予想生成
                prediction = generate_simple_prediction(race)
                crud.create_prediction(db, prediction)

        print(f"サンプルデータの生成完了！")

    finally:
        db.close()


if __name__ == "__main__":
    initialize_sample_data()
