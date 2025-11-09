"""
シンプルな予想モデル
後でLightGBMに置き換える予定
"""
from typing import List
import random
import uuid
from datetime import datetime

from app.models import Race, Prediction, Entry


def generate_simple_prediction(race: Race) -> Prediction:
    """
    シンプルなルールベース予想
    - オッズが低い（人気）馬を優先
    - オッズがない場合はランダム
    """
    entries = sorted(race.entries, key=lambda e: e.odds if e.odds else 999.0)

    # 人気上位3頭を選択（オッズ順）
    if len(entries) >= 3:
        first = entries[0].horse_number
        second = entries[1].horse_number
        third = entries[2].horse_number
    else:
        # 頭数が少ない場合
        horse_numbers = [e.horse_number for e in entries]
        random.shuffle(horse_numbers)
        first = horse_numbers[0] if len(horse_numbers) > 0 else 1
        second = horse_numbers[1] if len(horse_numbers) > 1 else 2
        third = horse_numbers[2] if len(horse_numbers) > 2 else 3

    # 信頼度は適当に設定（オッズから計算）
    confidence = 0.5 + (random.random() * 0.3)  # 0.5-0.8

    return Prediction(
        prediction_id=str(uuid.uuid4()),
        race_id=race.race_id,
        predicted_at=datetime.now(),
        first=first,
        second=second,
        third=third,
        confidence=confidence,
        model_version="simple-v1.0"
    )


def calculate_features(entry: Entry, race: Race) -> dict:
    """
    特徴量計算（将来のML用）
    """
    features = {
        "horse_number": entry.horse_number,
        "gate_number": entry.gate_number,
        "weight": entry.weight,
        "odds": entry.odds or 10.0,
        "age": entry.horse.age,
        "distance": race.distance,
    }

    # 過去成績から平均着順
    if entry.past_results:
        features["avg_past_finish"] = sum(entry.past_results) / len(entry.past_results)
    else:
        features["avg_past_finish"] = 5.0

    return features
