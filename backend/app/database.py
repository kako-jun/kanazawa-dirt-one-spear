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
    first = Column(Integer, nullable=False)
    second = Column(Integer, nullable=False)
    third = Column(Integer, nullable=False)
    payout_trifecta = Column(Integer, nullable=True)
    prediction_hit = Column(Boolean, nullable=False)
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
