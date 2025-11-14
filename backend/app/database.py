from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# データベースファイルのパス
from pathlib import Path
DB_DIR = Path(__file__).parent.parent / "data"
DB_DIR.mkdir(exist_ok=True)
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_DIR}/kanazawa_dirt_one_spear.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# データベースモデル

class DBJockey(Base):
    """騎手マスタテーブル"""
    __tablename__ = "jockeys"

    # 主キー
    jockey_id = Column(String, primary_key=True, index=True, comment="騎手ID")

    # 基本情報
    name = Column(String, nullable=False, unique=True, index=True, comment="騎手名")
    name_normalized = Column(String, nullable=True, index=True, comment="正規化名 (所属除去)")


class DBTrainer(Base):
    """調教師マスタテーブル"""
    __tablename__ = "trainers"

    # 主キー
    trainer_id = Column(String, primary_key=True, index=True, comment="調教師ID")

    # 基本情報
    name = Column(String, nullable=False, unique=True, index=True, comment="調教師名")


class DBHorse(Base):
    """馬マスタテーブル（完全正規化・系図対応）"""
    __tablename__ = "horses"

    # 主キー
    horse_id = Column(String, primary_key=True, index=True, comment="馬ID (名前_生年月日 or 名前のみ)")

    # 基本情報
    name = Column(String, nullable=False, index=True, comment="馬名")
    birth_date = Column(String, nullable=True, comment="生年月日 (例: 04.05生)")
    age = Column(Integer, nullable=True, comment="年齢（出走馬のみ）")
    gender = Column(String, nullable=True, comment="性別 (male/female/gelding)")
    coat_color = Column(String, nullable=True, comment="毛色")

    # 血統情報（正規化：FK）
    sire_id = Column(String, ForeignKey("horses.horse_id"), nullable=True, index=True, comment="父馬ID")
    dam_id = Column(String, ForeignKey("horses.horse_id"), nullable=True, index=True, comment="母馬ID")
    broodmare_sire_id = Column(String, ForeignKey("horses.horse_id"), nullable=True, index=True, comment="母父ID")
    breeder = Column(String, nullable=True, comment="生産者")

    # フラグ
    is_runner = Column(Boolean, default=False, nullable=False, comment="出走経験あり")

    # 自己参照リレーション（血統）
    sire = relationship("DBHorse", remote_side=[horse_id], foreign_keys=[sire_id], backref="children_as_sire")
    dam = relationship("DBHorse", remote_side=[horse_id], foreign_keys=[dam_id], backref="children_as_dam")
    broodmare_sire = relationship("DBHorse", remote_side=[horse_id], foreign_keys=[broodmare_sire_id], backref="children_as_broodmare_sire")


class DBRace(Base):
    """レーステーブル（正規化）"""
    __tablename__ = "races"

    # 主キー
    race_id = Column(String, primary_key=True, index=True, comment="レースID (YYYYMMDD_RR)")

    # 基本情報
    date = Column(DateTime, nullable=False, index=True, comment="開催日")
    race_number = Column(Integer, nullable=False, comment="レース番号")
    name = Column(String, nullable=False, comment="レース名")
    subtitle = Column(String, nullable=True, comment="サブタイトル (準重賞など)")

    # コース情報
    distance = Column(Integer, nullable=False, comment="距離 (m)")
    direction = Column(String, nullable=True, comment="コース方向 (左回り/右回り)")
    track_condition = Column(String, nullable=False, comment="馬場状態 (良/稍重/重/不良)")
    weather = Column(String, nullable=False, comment="天候 (晴/曇/雨/雪)")

    # レース条件
    race_class = Column(String, nullable=True, comment="馬級 (サラブレッド系/アングロアラブ系)")
    race_category = Column(String, nullable=True, comment="カテゴリ (一般/牝馬限定/若駒)")
    weight_system = Column(String, nullable=True, comment="重量方式 (定量/別定/ハンデ)")

    # その他
    prize_money = Column(JSON, nullable=True, comment="賞金情報 (JSON: {1着: 金額, ...})")
    betting_code = Column(String, nullable=True, comment="電話投票コード")

    # リレーション
    entries = relationship("DBEntry", back_populates="race", cascade="all, delete-orphan")
    prediction = relationship("DBPrediction", back_populates="race", uselist=False)
    result = relationship("DBResult", back_populates="race", uselist=False)


class DBEntry(Base):
    """出走情報テーブル（完全正規化）"""
    __tablename__ = "entries"

    # 主キー
    entry_id = Column(String, primary_key=True, index=True, comment="出走ID (race_id_horse_number)")

    # 外部キー
    race_id = Column(String, ForeignKey("races.race_id"), nullable=False, index=True, comment="レースID")
    horse_id = Column(String, ForeignKey("horses.horse_id"), nullable=False, index=True, comment="馬ID")
    jockey_id = Column(String, ForeignKey("jockeys.jockey_id"), nullable=False, index=True, comment="騎手ID")
    trainer_id = Column(String, ForeignKey("trainers.trainer_id"), nullable=True, index=True, comment="調教師ID")

    # 出走情報
    gate_number = Column(Integer, nullable=False, comment="枠番")
    horse_number = Column(Integer, nullable=False, comment="馬番")

    # 重量情報
    weight = Column(Float, nullable=False, comment="斤量 (kg)")
    horse_weight = Column(Integer, nullable=True, comment="馬体重 (kg)")
    weight_diff = Column(String, nullable=True, comment="馬体重増減 (例: +4, -2)")

    # 実績情報（このエントリ時点のもの）
    career_record = Column(String, nullable=True, comment="通算成績 (例: 0-1-2-22)")
    detailed_record = Column(JSON, nullable=True, comment="着別成績詳細 (JSON: {all:{}, left:{}, ...})")
    best_time = Column(String, nullable=True, comment="最高タイム (例: 1:29.9)")
    best_time_good_track = Column(String, nullable=True, comment="良馬場最高タイム (例: 良1:31.3)")
    past_results = Column(JSON, nullable=True, comment="過去5走詳細 (JSON配列)")

    # オッズ
    odds = Column(Float, nullable=True, comment="オッズ")

    # リレーション
    race = relationship("DBRace", back_populates="entries")
    horse = relationship("DBHorse")
    jockey = relationship("DBJockey")
    trainer = relationship("DBTrainer")


class DBPrediction(Base):
    """予想テーブル"""
    __tablename__ = "predictions"

    # 主キー
    prediction_id = Column(String, primary_key=True, index=True, comment="予想ID")

    # 外部キー
    race_id = Column(String, ForeignKey("races.race_id"), nullable=False, unique=True, index=True, comment="レースID (1レース1予想)")

    # 予想内容
    first = Column(Integer, nullable=False, comment="1着予想馬番")
    second = Column(Integer, nullable=False, comment="2着予想馬番")
    third = Column(Integer, nullable=False, comment="3着予想馬番")
    confidence = Column(Float, nullable=False, comment="信頼度 (0.0-1.0)")

    # メタ情報
    model_version = Column(String, nullable=False, comment="モデルバージョン")
    predicted_at = Column(DateTime, nullable=False, default=datetime.now, comment="予想日時")

    # リレーション
    race = relationship("DBRace", back_populates="prediction")


class DBResult(Base):
    """結果テーブル"""
    __tablename__ = "results"

    # 主キー
    result_id = Column(String, primary_key=True, index=True, comment="結果ID")

    # 外部キー
    race_id = Column(String, ForeignKey("races.race_id"), nullable=False, unique=True, index=True, comment="レースID (1レース1結果)")

    # 着順情報
    finish_order = Column(JSON, nullable=True, comment="全着順 (JSON配列: [1位馬番, 2位馬番, ...])")
    first = Column(Integer, nullable=True, comment="1着馬番")
    second = Column(Integer, nullable=True, comment="2着馬番")
    third = Column(Integer, nullable=True, comment="3着馬番")

    # レース展開
    corner_positions = Column(JSON, nullable=True, comment="コーナー通過順 (JSON: {corner_1: '7,9,1,...', ...})")

    # 配当情報
    payouts = Column(JSON, nullable=True, comment="全配当 (JSON: {win: {...}, place: {...}, trifecta: {...}, ...})")
    payout_trifecta = Column(Integer, nullable=True, comment="三連単配当 (円)")

    # 予想結果
    prediction_hit = Column(Boolean, nullable=False, default=False, comment="予想的中フラグ")

    # 購入情報
    purchased = Column(Boolean, nullable=False, default=False, comment="実購入フラグ")
    bet_amount = Column(Integer, nullable=True, comment="購入金額 (円)")
    return_amount = Column(Integer, nullable=True, comment="払戻金額 (円)")

    # メタ情報
    recorded_at = Column(DateTime, nullable=False, default=datetime.now, index=True, comment="記録日時")
    memo = Column(Text, nullable=True, comment="メモ")

    # リレーション
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
