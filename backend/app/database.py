from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# データベースファイルのパス
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./kanazawa_dirt_one_spear.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# データベースモデル
class DBHorse(Base):
    __tablename__ = "horses"

    horse_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)


class DBRace(Base):
    __tablename__ = "races"

    race_id = Column(String, primary_key=True, index=True)
    date = Column(DateTime, nullable=False, index=True)
    race_number = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    distance = Column(Integer, nullable=False)
    track_condition = Column(String, nullable=False)
    weather = Column(String, nullable=False)
    direction = Column(String, nullable=True)  # 左回り/右回り

    entries = relationship("DBEntry", back_populates="race", cascade="all, delete-orphan")
    prediction = relationship("DBPrediction", back_populates="race", uselist=False)
    result = relationship("DBResult", back_populates="race", uselist=False)


class DBEntry(Base):
    __tablename__ = "entries"

    entry_id = Column(String, primary_key=True, index=True)
    race_id = Column(String, ForeignKey("races.race_id"), nullable=False, index=True)
    horse_id = Column(String, ForeignKey("horses.horse_id"), nullable=False)
    gate_number = Column(Integer, nullable=False)
    horse_number = Column(Integer, nullable=False)
    jockey = Column(String, nullable=False)
    weight = Column(Float, nullable=False)
    odds = Column(Float, nullable=True)
    past_results = Column(JSON, nullable=True)

    race = relationship("DBRace", back_populates="entries")
    horse = relationship("DBHorse")


class DBPrediction(Base):
    __tablename__ = "predictions"

    prediction_id = Column(String, primary_key=True, index=True)
    race_id = Column(String, ForeignKey("races.race_id"), nullable=False, unique=True, index=True)
    predicted_at = Column(DateTime, nullable=False, default=datetime.now)
    first = Column(Integer, nullable=False)
    second = Column(Integer, nullable=False)
    third = Column(Integer, nullable=False)
    confidence = Column(Float, nullable=False)
    model_version = Column(String, nullable=False)

    race = relationship("DBRace", back_populates="prediction")


class DBResult(Base):
    __tablename__ = "results"

    result_id = Column(String, primary_key=True, index=True)
    race_id = Column(String, ForeignKey("races.race_id"), nullable=False, unique=True, index=True)

    # 全着順（JSON配列で保存: [1位馬番, 2位馬番, ...]）
    finish_order = Column(JSON, nullable=True)

    # コーナー通過順（JSON形式: {corner_1: "7,9,1,...", corner_2: "7,9,1,...", ...}）
    corner_positions = Column(JSON, nullable=True)

    # 1-3着（後方互換性のため残す）
    first = Column(Integer, nullable=True)
    second = Column(Integer, nullable=True)
    third = Column(Integer, nullable=True)

    # 全配当（JSON形式で保存）
    payouts = Column(JSON, nullable=True)  # {win: {...}, place: {...}, exacta: {...}, trifecta: {...}, etc}

    # 三連単配当（後方互換性のため残す）
    payout_trifecta = Column(Integer, nullable=True)

    # 予想関連
    prediction_hit = Column(Boolean, nullable=False, default=False)
    purchased = Column(Boolean, nullable=False, default=False)
    bet_amount = Column(Integer, nullable=True)
    return_amount = Column(Integer, nullable=True)
    recorded_at = Column(DateTime, nullable=False, default=datetime.now, index=True)
    memo = Column(Text, nullable=True)

    race = relationship("DBRace", back_populates="result")


# データベース初期化
def init_db():
    Base.metadata.create_all(bind=engine)


# DBセッション取得
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
