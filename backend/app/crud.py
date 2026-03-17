from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uuid

from app.database import DBRace, DBEntry, DBHorse, DBPrediction, DBResult, DBJockey
from app.models import Race, Entry, Horse, Prediction, Result, ResultSubmit


# Jockey helper
def get_or_create_jockey_id(db: Session, jockey_name: str) -> str:
    """騎手名からjockey_idを取得、存在しなければ作成"""
    import re
    jockey_id = f"jockey_{jockey_name}"
    existing = db.query(DBJockey).filter(DBJockey.jockey_id == jockey_id).first()
    if not existing:
        normalized = re.sub(r'\([^)]*\)', '', jockey_name).strip()
        db.add(DBJockey(jockey_id=jockey_id, name=jockey_name, name_normalized=normalized))
        db.flush()
    return jockey_id


# Horse CRUD
def create_horse(db: Session, horse: Horse) -> DBHorse:
    db_horse = DBHorse(**horse.model_dump())
    db.add(db_horse)
    db.commit()
    db.refresh(db_horse)
    return db_horse


def get_or_create_horse(db: Session, horse: Horse) -> DBHorse:
    db_horse = db.query(DBHorse).filter(DBHorse.horse_id == horse.horse_id).first()
    if not db_horse:
        db_horse = create_horse(db, horse)
    return db_horse


# Race CRUD
def create_race(db: Session, race: Race) -> DBRace:
    # 馬を先に作成
    horses = []
    for entry in race.entries:
        horse = get_or_create_horse(db, entry.horse)
        horses.append(horse)

    # レース作成
    db_race = DBRace(
        race_id=race.race_id,
        date=race.date,
        race_number=race.race_number,
        name=race.name,
        distance=race.distance,
        track_condition=race.track_condition,
        weather=race.weather,
    )
    db.add(db_race)
    db.flush()

    # エントリー作成
    for entry in race.entries:
        jockey_id = get_or_create_jockey_id(db, entry.jockey)
        db_entry = DBEntry(
            entry_id=entry.entry_id,
            race_id=race.race_id,
            horse_id=entry.horse.horse_id,
            jockey_id=jockey_id,
            gate_number=entry.gate_number,
            horse_number=entry.horse_number,
            weight=entry.weight,
            odds=entry.odds,
            past_results=entry.past_results,
        )
        db.add(db_entry)

    db.commit()
    db.refresh(db_race)
    return db_race


def get_races(db: Session, date: Optional[str] = None) -> List[Race]:
    query = db.query(DBRace)
    if date:
        target_date = datetime.fromisoformat(date).date()
        query = query.filter(DBRace.date >= datetime.combine(target_date, datetime.min.time()))
        query = query.filter(DBRace.date < datetime.combine(target_date, datetime.max.time()))

    db_races = query.order_by(DBRace.date, DBRace.race_number).all()
    return [db_race_to_model(db, db_race) for db_race in db_races]


def get_race(db: Session, race_id: str) -> Optional[Race]:
    db_race = db.query(DBRace).filter(DBRace.race_id == race_id).first()
    if not db_race:
        return None
    return db_race_to_model(db, db_race)


def db_race_to_model(db: Session, db_race: DBRace) -> Race:
    entries = []
    for db_entry in db_race.entries:
        # horse relationship may be None if the FK row is missing
        if db_entry.horse is None:
            continue
        horse = Horse(
            horse_id=db_entry.horse.horse_id,
            name=db_entry.horse.name,
            age=db_entry.horse.age or 0,
            gender=db_entry.horse.gender or "不明",
        )
        # jockey relationship may be None if FK row missing; fall back to jockey_id string
        jockey_name = (
            db_entry.jockey.name if db_entry.jockey else db_entry.jockey_id or "不明"
        )
        entry = Entry(
            entry_id=db_entry.entry_id,
            race_id=db_entry.race_id,
            horse=horse,
            gate_number=db_entry.gate_number,
            horse_number=db_entry.horse_number,
            jockey=jockey_name,
            weight=db_entry.weight,
            odds=db_entry.odds,
            past_results=db_entry.past_results or [],
        )
        entries.append(entry)

    return Race(
        race_id=db_race.race_id,
        date=db_race.date,
        race_number=db_race.race_number,
        name=db_race.name,
        distance=db_race.distance,
        track_condition=db_race.track_condition,
        weather=db_race.weather,
        entries=entries,
    )


# Prediction CRUD
def create_prediction(db: Session, prediction: Prediction) -> DBPrediction:
    db_prediction = DBPrediction(**prediction.model_dump())
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction


def get_prediction(db: Session, race_id: str) -> Optional[Prediction]:
    db_prediction = db.query(DBPrediction).filter(DBPrediction.race_id == race_id).first()
    if not db_prediction:
        return None
    return Prediction(
        prediction_id=db_prediction.prediction_id,
        race_id=db_prediction.race_id,
        predicted_at=db_prediction.predicted_at,
        first=db_prediction.first,
        second=db_prediction.second,
        third=db_prediction.third,
        confidence=db_prediction.confidence,
        model_version=db_prediction.model_version,
    )


# Result CRUD
def create_result(db: Session, result_submit: ResultSubmit) -> Result:
    # 予想取得
    prediction = get_prediction(db, result_submit.race_id)
    if not prediction:
        raise ValueError("予想が見つかりません")

    # 的中判定
    prediction_hit = (
        prediction.first == result_submit.first and
        prediction.second == result_submit.second and
        prediction.third == result_submit.third
    )

    # 払戻金額計算
    return_amount = 0
    if prediction_hit and result_submit.purchased and result_submit.bet_amount:
        if result_submit.payout_trifecta:
            return_amount = (result_submit.bet_amount // 100) * result_submit.payout_trifecta

    result_id = str(uuid.uuid4())
    db_result = DBResult(
        result_id=result_id,
        race_id=result_submit.race_id,
        first=result_submit.first,
        second=result_submit.second,
        third=result_submit.third,
        payout_trifecta=result_submit.payout_trifecta,
        prediction_hit=prediction_hit,
        purchased=result_submit.purchased,
        bet_amount=result_submit.bet_amount,
        return_amount=return_amount,
        recorded_at=datetime.now(),
        memo=result_submit.memo,
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)

    return _db_result_to_model(db_result)


def _db_result_to_model(db_result: DBResult) -> Result:
    return Result(
        result_id=db_result.result_id,
        race_id=db_result.race_id,
        first=db_result.first,
        second=db_result.second,
        third=db_result.third,
        payout_trifecta=db_result.payout_trifecta,
        prediction_hit=db_result.prediction_hit,
        purchased=db_result.purchased,
        bet_amount=db_result.bet_amount,
        return_amount=db_result.return_amount,
        recorded_at=db_result.recorded_at,
        memo=db_result.memo,
    )


def get_results(db: Session) -> List[Result]:
    db_results = db.query(DBResult).order_by(DBResult.recorded_at.desc()).all()
    return [_db_result_to_model(r) for r in db_results]
