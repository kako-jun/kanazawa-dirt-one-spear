from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class Horse(BaseModel):
    """馬の基本情報"""
    horse_id: str
    name: str
    age: int
    gender: str  # 牡, 牝, セン


class Entry(BaseModel):
    """出走情報"""
    entry_id: str
    race_id: str
    horse: Horse
    gate_number: int = Field(..., description="枠番")
    horse_number: int = Field(..., description="馬番")
    jockey: str = Field(..., description="騎手名")
    weight: float = Field(..., description="斤量")
    odds: Optional[float] = Field(None, description="単勝オッズ")
    past_results: Optional[List[int]] = Field(default=[], description="過去5走の着順")


class Race(BaseModel):
    """レース情報"""
    race_id: str
    date: datetime
    race_number: int = Field(..., description="第何レース")
    name: str = Field(..., description="レース名")
    distance: int = Field(..., description="距離（メートル）")
    track_condition: str = Field(..., description="馬場状態（良、稍重、重、不良）")
    weather: str = Field(..., description="天候")
    entries: List[Entry] = Field(default=[], description="出走馬リスト")


class Prediction(BaseModel):
    """予想（3連単1本）"""
    prediction_id: str
    race_id: str
    predicted_at: datetime
    first: int = Field(..., description="1着予想馬番")
    second: int = Field(..., description="2着予想馬番")
    third: int = Field(..., description="3着予想馬番")
    confidence: float = Field(..., description="信頼度（0-1）")
    model_version: str = Field(..., description="使用モデルバージョン")


class Result(BaseModel):
    """レース結果"""
    result_id: str
    race_id: str
    first: int = Field(..., description="1着馬番")
    second: int = Field(..., description="2着馬番")
    third: int = Field(..., description="3着馬番")
    payout_trifecta: Optional[int] = Field(None, description="3連単配当")
    prediction_hit: bool = Field(..., description="予想的中フラグ")
    purchased: bool = Field(default=False, description="実際に購入したか")
    bet_amount: Optional[int] = Field(None, description="購入金額（円）")
    return_amount: Optional[int] = Field(None, description="払戻金額（円）")
    recorded_at: datetime = Field(default_factory=datetime.now, description="記録日時")
    memo: Optional[str] = Field(None, description="メモ・感想")


class ResultSubmit(BaseModel):
    """結果投稿用モデル"""
    race_id: str
    first: int
    second: int
    third: int
    payout_trifecta: Optional[int] = None
    purchased: bool = False
    bet_amount: Optional[int] = None
    memo: Optional[str] = None


class Statistics(BaseModel):
    """統計情報"""
    total_races: int = Field(..., description="総レース数")
    total_predictions: int = Field(..., description="総予想数")
    hit_count: int = Field(..., description="的中数")
    hit_rate: float = Field(..., description="的中率")
    purchased_count: int = Field(default=0, description="実購入数")
    purchased_hit_count: int = Field(default=0, description="実購入的中数")
    purchased_hit_rate: float = Field(default=0.0, description="実購入的中率")
    roi: float = Field(..., description="回収率（%）")
    total_investment: int = Field(..., description="総投資額（円）")
    total_return: int = Field(..., description="総払戻額（円）")
    profit: int = Field(default=0, description="収支（円）")
    max_payout: int = Field(default=0, description="最高配当（円）")
    recent_results: List[str] = Field(default=[], description="直近10件の結果（◯×）")
