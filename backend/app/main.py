from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session

from app.models import Race, Prediction, Statistics, Result, ResultSubmit
from app.database import init_db, get_db
from app import crud
from app.predictor import generate_simple_prediction

app = FastAPI(
    title="金沢ダート一本槍 API",
    description="Kanazawa Dirt One Spear - 金沢競馬AI予想システム",
    version="0.1.0",
)

# データベース初期化
@app.on_event("startup")
def startup_event():
    init_db()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def root():
    return {
        "message": "金沢ダート一本槍 API",
        "description": "金沢競馬AI予想システム - 趣味・無料・応援目的",
        "version": "0.1.0"
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/api/races", response_model=List[Race])
async def get_races(date: str = None, db: Session = Depends(get_db)):
    """レース一覧を取得"""
    return crud.get_races(db, date)


@app.get("/api/races/{race_id}", response_model=Race)
async def get_race(race_id: str, db: Session = Depends(get_db)):
    """レース詳細を取得"""
    race = crud.get_race(db, race_id)
    if not race:
        raise HTTPException(status_code=404, detail="レースが見つかりません")
    return race


@app.get("/api/predictions/{race_id}", response_model=Prediction)
async def get_prediction(race_id: str, db: Session = Depends(get_db)):
    """予想を取得（3連単1本）"""
    race = crud.get_race(db, race_id)
    if not race:
        raise HTTPException(status_code=404, detail="レースが見つかりません")

    prediction = crud.get_prediction(db, race_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="予想がまだ生成されていません")

    return prediction


@app.get("/api/results", response_model=List[Result])
async def get_results(db: Session = Depends(get_db)):
    """結果一覧を取得"""
    return crud.get_results(db)


@app.post("/api/results", response_model=Result)
async def submit_result(result_submit: ResultSubmit, db: Session = Depends(get_db)):
    """結果を投稿"""
    race = crud.get_race(db, result_submit.race_id)
    if not race:
        raise HTTPException(status_code=404, detail="レースが見つかりません")

    try:
        result = crud.create_result(db, result_submit)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/stats", response_model=Statistics)
async def get_statistics(db: Session = Depends(get_db)):
    """統計情報を取得"""
    all_results = crud.get_results(db)

    if not all_results:
        return Statistics(
            total_races=0,
            total_predictions=0,
            hit_count=0,
            hit_rate=0.0,
            purchased_count=0,
            purchased_hit_count=0,
            purchased_hit_rate=0.0,
            roi=0.0,
            total_investment=0,
            total_return=0,
            profit=0,
            max_payout=0,
            recent_results=[]
        )

    # 統計計算
    total_predictions = len(all_results)
    hit_count = sum(1 for r in all_results if r.prediction_hit)
    hit_rate = (hit_count / total_predictions * 100) if total_predictions > 0 else 0.0

    # 実購入の統計
    purchased_results = [r for r in all_results if r.purchased]
    purchased_count = len(purchased_results)
    purchased_hit_count = sum(1 for r in purchased_results if r.prediction_hit)
    purchased_hit_rate = (purchased_hit_count / purchased_count * 100) if purchased_count > 0 else 0.0

    # 金額計算
    total_investment = sum(r.bet_amount or 0 for r in purchased_results)
    total_return = sum(r.return_amount or 0 for r in purchased_results)
    profit = total_return - total_investment
    roi = (total_return / total_investment * 100) if total_investment > 0 else 0.0

    # 最高配当
    max_payout = max((r.payout_trifecta or 0 for r in all_results), default=0)

    # 直近10件の結果
    sorted_results = sorted(all_results, key=lambda x: x.recorded_at, reverse=True)[:10]
    recent_results = ["◯" if r.prediction_hit else "×" for r in sorted_results]

    total_races = len(crud.get_races(db))

    return Statistics(
        total_races=total_races,
        total_predictions=total_predictions,
        hit_count=hit_count,
        hit_rate=hit_rate,
        purchased_count=purchased_count,
        purchased_hit_count=purchased_hit_count,
        purchased_hit_rate=purchased_hit_rate,
        roi=roi,
        total_investment=total_investment,
        total_return=total_return,
        profit=profit,
        max_payout=max_payout,
        recent_results=recent_results
    )


# 管理用API
@app.post("/api/admin/races", response_model=Race)
async def create_race_endpoint(race: Race, db: Session = Depends(get_db)):
    """レースを登録"""
    db_race = crud.create_race(db, race)
    return crud.get_race(db, db_race.race_id)


@app.post("/api/admin/predictions/{race_id}", response_model=Prediction)
async def generate_prediction_endpoint(race_id: str, db: Session = Depends(get_db)):
    """予想を生成"""
    race = crud.get_race(db, race_id)
    if not race:
        raise HTTPException(status_code=404, detail="レースが見つかりません")

    # 既に予想がある場合はエラー
    existing_prediction = crud.get_prediction(db, race_id)
    if existing_prediction:
        raise HTTPException(status_code=400, detail="既に予想が存在します")

    # 予想生成
    prediction = generate_simple_prediction(race)
    db_prediction = crud.create_prediction(db, prediction)

    return crud.get_prediction(db, race_id)
