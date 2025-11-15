#!/usr/bin/env python3
"""
統計テーブル構築スクリプト

基本テーブル（races, horses, jockeys, trainers, race_performances）から
統計テーブル（stat_* プリフィックス）を構築する。

Usage:
    python build_stats_tables.py [--drop]

Options:
    --drop: 既存の統計テーブルを削除してから再構築
"""

import sys
import sqlite3
from pathlib import Path
import argparse
from datetime import datetime

DB_PATH = Path(__file__).parent / "data" / "kanazawa_dirt_one_spear.db"


def get_connection():
    """DB接続を取得"""
    return sqlite3.connect(DB_PATH)


def drop_stats_tables(conn):
    """すべての統計テーブルを削除"""
    print("Dropping existing stats tables...")

    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stat_%'")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        print(f"  Dropping {table_name}...")
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    conn.commit()
    print(f"Dropped {len(tables)} stats tables\n")


def create_stat_horse_cumulative(conn):
    """馬の累積成績テーブルを作成"""
    print("Creating stat_horse_cumulative...")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS stat_horse_cumulative (
            horse_id VARCHAR NOT NULL,
            as_of_date DATE NOT NULL,
            total_races INTEGER,
            wins INTEGER,
            places INTEGER,
            win_rate REAL,
            place_rate REAL,
            avg_finish_position REAL,
            days_since_last_race INTEGER,
            PRIMARY KEY (horse_id, as_of_date)
        )
    """)

    conn.execute("CREATE INDEX IF NOT EXISTS idx_horse_cum_date ON stat_horse_cumulative(as_of_date)")

    # データ投入 - DISTINCTで同日の重複を除去
    conn.execute("""
        INSERT INTO stat_horse_cumulative
        SELECT DISTINCT
            horse_id,
            race_date as as_of_date,
            total_races,
            wins,
            places,
            win_rate,
            place_rate,
            avg_finish_position,
            days_since_last_race
        FROM (
            SELECT
                horse_id,
                race_date,
                COUNT(*) OVER (PARTITION BY horse_id ORDER BY race_date) as total_races,
                SUM(CASE WHEN finish_position = 1 THEN 1 ELSE 0 END)
                    OVER (PARTITION BY horse_id ORDER BY race_date) as wins,
                SUM(CASE WHEN finish_position <= 3 THEN 1 ELSE 0 END)
                    OVER (PARTITION BY horse_id ORDER BY race_date) as places,
                CAST(SUM(CASE WHEN finish_position = 1 THEN 1 ELSE 0 END)
                    OVER (PARTITION BY horse_id ORDER BY race_date) AS REAL) /
                    NULLIF(COUNT(*) OVER (PARTITION BY horse_id ORDER BY race_date), 0) as win_rate,
                CAST(SUM(CASE WHEN finish_position <= 3 THEN 1 ELSE 0 END)
                    OVER (PARTITION BY horse_id ORDER BY race_date) AS REAL) /
                    NULLIF(COUNT(*) OVER (PARTITION BY horse_id ORDER BY race_date), 0) as place_rate,
                AVG(finish_position) OVER (PARTITION BY horse_id ORDER BY race_date) as avg_finish_position,
                JULIANDAY(race_date) - LAG(JULIANDAY(race_date)) OVER (PARTITION BY horse_id ORDER BY race_date) as days_since_last_race
            FROM (
                SELECT
                    rp.horse_id,
                    r.date as race_date,
                    rp.finish_position
                FROM race_performances rp
                JOIN races r ON rp.race_id = r.race_id
                WHERE rp.finish_position IS NOT NULL
                ORDER BY rp.horse_id, r.date
            )
        )
    """)

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM stat_horse_cumulative").fetchone()[0]
    print(f"  Inserted {count} rows\n")


def create_stat_jockey_cumulative(conn):
    """騎手の累積成績テーブルを作成"""
    print("Creating stat_jockey_cumulative...")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS stat_jockey_cumulative (
            jockey_id VARCHAR NOT NULL,
            as_of_date DATE NOT NULL,
            total_races INTEGER,
            wins INTEGER,
            places INTEGER,
            win_rate REAL,
            place_rate REAL,
            avg_finish_position REAL,
            PRIMARY KEY (jockey_id, as_of_date)
        )
    """)

    conn.execute("CREATE INDEX IF NOT EXISTS idx_jockey_cum_date ON stat_jockey_cumulative(as_of_date)")

    conn.execute("""
        INSERT INTO stat_jockey_cumulative
        SELECT DISTINCT
            jockey_id,
            race_date as as_of_date,
            total_races,
            wins,
            places,
            win_rate,
            place_rate,
            avg_finish_position
        FROM (
            SELECT
                jockey_id,
                race_date,
                COUNT(*) OVER (PARTITION BY jockey_id ORDER BY race_date) as total_races,
                SUM(CASE WHEN finish_position = 1 THEN 1 ELSE 0 END)
                    OVER (PARTITION BY jockey_id ORDER BY race_date) as wins,
                SUM(CASE WHEN finish_position <= 3 THEN 1 ELSE 0 END)
                    OVER (PARTITION BY jockey_id ORDER BY race_date) as places,
                CAST(SUM(CASE WHEN finish_position = 1 THEN 1 ELSE 0 END)
                    OVER (PARTITION BY jockey_id ORDER BY race_date) AS REAL) /
                    NULLIF(COUNT(*) OVER (PARTITION BY jockey_id ORDER BY race_date), 0) as win_rate,
                CAST(SUM(CASE WHEN finish_position <= 3 THEN 1 ELSE 0 END)
                    OVER (PARTITION BY jockey_id ORDER BY race_date) AS REAL) /
                    NULLIF(COUNT(*) OVER (PARTITION BY jockey_id ORDER BY race_date), 0) as place_rate,
                AVG(finish_position) OVER (PARTITION BY jockey_id ORDER BY race_date) as avg_finish_position
            FROM (
                SELECT
                    e.jockey_id,
                    r.date as race_date,
                    rp.finish_position
                FROM race_performances rp
                JOIN races r ON rp.race_id = r.race_id
                JOIN entries e ON rp.entry_id = e.entry_id
                WHERE rp.finish_position IS NOT NULL
                ORDER BY e.jockey_id, r.date
            )
        )
    """)

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM stat_jockey_cumulative").fetchone()[0]
    print(f"  Inserted {count} rows\n")


def create_stat_trainer_cumulative(conn):
    """調教師の累積成績テーブルを作成"""
    print("Creating stat_trainer_cumulative...")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS stat_trainer_cumulative (
            trainer_id VARCHAR NOT NULL,
            as_of_date DATE NOT NULL,
            total_races INTEGER,
            wins INTEGER,
            places INTEGER,
            win_rate REAL,
            place_rate REAL,
            PRIMARY KEY (trainer_id, as_of_date)
        )
    """)

    conn.execute("CREATE INDEX IF NOT EXISTS idx_trainer_cum_date ON stat_trainer_cumulative(as_of_date)")

    conn.execute("""
        INSERT INTO stat_trainer_cumulative
        SELECT DISTINCT
            trainer_id,
            race_date as as_of_date,
            total_races,
            wins,
            places,
            win_rate,
            place_rate
        FROM (
            SELECT
                trainer_id,
                race_date,
                COUNT(*) OVER (PARTITION BY trainer_id ORDER BY race_date) as total_races,
                SUM(CASE WHEN finish_position = 1 THEN 1 ELSE 0 END)
                    OVER (PARTITION BY trainer_id ORDER BY race_date) as wins,
                SUM(CASE WHEN finish_position <= 3 THEN 1 ELSE 0 END)
                    OVER (PARTITION BY trainer_id ORDER BY race_date) as places,
                CAST(SUM(CASE WHEN finish_position = 1 THEN 1 ELSE 0 END)
                    OVER (PARTITION BY trainer_id ORDER BY race_date) AS REAL) /
                    NULLIF(COUNT(*) OVER (PARTITION BY trainer_id ORDER BY race_date), 0) as win_rate,
                CAST(SUM(CASE WHEN finish_position <= 3 THEN 1 ELSE 0 END)
                    OVER (PARTITION BY trainer_id ORDER BY race_date) AS REAL) /
                    NULLIF(COUNT(*) OVER (PARTITION BY trainer_id ORDER BY race_date), 0) as place_rate
            FROM (
                SELECT
                    e.trainer_id,
                    r.date as race_date,
                    rp.finish_position
                FROM race_performances rp
                JOIN races r ON rp.race_id = r.race_id
                JOIN entries e ON rp.entry_id = e.entry_id
                WHERE rp.finish_position IS NOT NULL
                ORDER BY e.trainer_id, r.date
            )
        )
    """)

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM stat_trainer_cumulative").fetchone()[0]
    print(f"  Inserted {count} rows\n")


def create_stat_horse_jockey_combo(conn):
    """馬×騎手の相性統計テーブルを作成"""
    print("Creating stat_horse_jockey_combo...")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS stat_horse_jockey_combo (
            horse_id VARCHAR NOT NULL,
            jockey_id VARCHAR NOT NULL,
            total_races INTEGER,
            wins INTEGER,
            places INTEGER,
            win_rate REAL,
            place_rate REAL,
            avg_finish_position REAL,
            first_race_date DATE,
            last_race_date DATE,
            PRIMARY KEY (horse_id, jockey_id)
        )
    """)

    conn.execute("""
        INSERT INTO stat_horse_jockey_combo
        SELECT
            rp.horse_id,
            e.jockey_id,
            COUNT(*) as total_races,
            SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) as wins,
            SUM(CASE WHEN rp.finish_position <= 3 THEN 1 ELSE 0 END) as places,
            CAST(SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) AS REAL) / COUNT(*) as win_rate,
            CAST(SUM(CASE WHEN rp.finish_position <= 3 THEN 1 ELSE 0 END) AS REAL) / COUNT(*) as place_rate,
            AVG(rp.finish_position) as avg_finish_position,
            MIN(r.date) as first_race_date,
            MAX(r.date) as last_race_date
        FROM race_performances rp
        JOIN races r ON rp.race_id = r.race_id
        JOIN entries e ON rp.entry_id = e.entry_id
        WHERE rp.finish_position IS NOT NULL
        GROUP BY rp.horse_id, e.jockey_id
        HAVING COUNT(*) >= 3
    """)

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM stat_horse_jockey_combo").fetchone()[0]
    print(f"  Inserted {count} rows\n")


def create_stat_horse_track_condition(conn):
    """馬ごとの馬場適性統計テーブルを作成"""
    print("Creating stat_horse_track_condition...")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS stat_horse_track_condition (
            horse_id VARCHAR NOT NULL,
            track_condition VARCHAR NOT NULL,
            total_races INTEGER,
            wins INTEGER,
            win_rate REAL,
            avg_finish_position REAL,
            PRIMARY KEY (horse_id, track_condition)
        )
    """)

    conn.execute("""
        INSERT INTO stat_horse_track_condition
        SELECT
            rp.horse_id,
            r.track_condition,
            COUNT(*) as total_races,
            SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) as wins,
            CAST(SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) AS REAL) / COUNT(*) as win_rate,
            AVG(rp.finish_position) as avg_finish_position
        FROM race_performances rp
        JOIN races r ON rp.race_id = r.race_id
        WHERE rp.finish_position IS NOT NULL
        GROUP BY rp.horse_id, r.track_condition
        HAVING COUNT(*) >= 2
    """)

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM stat_horse_track_condition").fetchone()[0]
    print(f"  Inserted {count} rows\n")


def create_stat_popularity_performance(conn):
    """人気ランク別の成績統計テーブルを作成"""
    print("Creating stat_popularity_performance...")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS stat_popularity_performance (
            popularity INTEGER NOT NULL,
            total_races INTEGER,
            wins INTEGER,
            places INTEGER,
            win_rate REAL,
            place_rate REAL,
            PRIMARY KEY (popularity)
        )
    """)

    conn.execute("""
        INSERT INTO stat_popularity_performance
        SELECT
            popularity,
            COUNT(*) as total_races,
            SUM(CASE WHEN finish_position = 1 THEN 1 ELSE 0 END) as wins,
            SUM(CASE WHEN finish_position <= 3 THEN 1 ELSE 0 END) as places,
            CAST(SUM(CASE WHEN finish_position = 1 THEN 1 ELSE 0 END) AS REAL) / COUNT(*) as win_rate,
            CAST(SUM(CASE WHEN finish_position <= 3 THEN 1 ELSE 0 END) AS REAL) / COUNT(*) as place_rate
        FROM race_performances
        WHERE finish_position IS NOT NULL AND popularity IS NOT NULL
        GROUP BY popularity
        ORDER BY popularity
    """)

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM stat_popularity_performance").fetchone()[0]
    print(f"  Inserted {count} rows\n")


def create_stat_horse_trainer_combo(conn):
    """馬×調教師の統計テーブルを作成"""
    print("Creating stat_horse_trainer_combo...")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS stat_horse_trainer_combo (
            horse_id VARCHAR NOT NULL,
            trainer_id VARCHAR NOT NULL,
            total_races INTEGER,
            wins INTEGER,
            places INTEGER,
            win_rate REAL,
            PRIMARY KEY (horse_id, trainer_id)
        )
    """)

    conn.execute("""
        INSERT INTO stat_horse_trainer_combo
        SELECT
            rp.horse_id,
            e.trainer_id,
            COUNT(*) as total_races,
            SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) as wins,
            SUM(CASE WHEN rp.finish_position <= 3 THEN 1 ELSE 0 END) as places,
            CAST(SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) AS REAL) / COUNT(*) as win_rate
        FROM race_performances rp
        JOIN entries e ON rp.entry_id = e.entry_id
        WHERE rp.finish_position IS NOT NULL AND e.trainer_id IS NOT NULL
        GROUP BY rp.horse_id, e.trainer_id
        HAVING COUNT(*) >= 2
    """)

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM stat_horse_trainer_combo").fetchone()[0]
    print(f"  Inserted {count} rows\n")


def create_stat_jockey_trainer_combo(conn):
    """騎手×調教師の連携統計テーブルを作成"""
    print("Creating stat_jockey_trainer_combo...")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS stat_jockey_trainer_combo (
            jockey_id VARCHAR NOT NULL,
            trainer_id VARCHAR NOT NULL,
            total_races INTEGER,
            wins INTEGER,
            places INTEGER,
            win_rate REAL,
            PRIMARY KEY (jockey_id, trainer_id)
        )
    """)

    conn.execute("""
        INSERT INTO stat_jockey_trainer_combo
        SELECT
            e.jockey_id,
            e.trainer_id,
            COUNT(*) as total_races,
            SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) as wins,
            SUM(CASE WHEN rp.finish_position <= 3 THEN 1 ELSE 0 END) as places,
            CAST(SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) AS REAL) / COUNT(*) as win_rate
        FROM entries e
        JOIN race_performances rp ON e.entry_id = rp.entry_id
        WHERE rp.finish_position IS NOT NULL AND e.trainer_id IS NOT NULL
        GROUP BY e.jockey_id, e.trainer_id
        HAVING COUNT(*) >= 5
    """)

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM stat_jockey_trainer_combo").fetchone()[0]
    print(f"  Inserted {count} rows\n")


def create_stat_horse_distance_category(conn):
    """距離適性統計テーブルを作成"""
    print("Creating stat_horse_distance_category...")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS stat_horse_distance_category (
            horse_id VARCHAR NOT NULL,
            distance_category VARCHAR NOT NULL,
            total_races INTEGER,
            wins INTEGER,
            win_rate REAL,
            avg_finish_position REAL,
            PRIMARY KEY (horse_id, distance_category)
        )
    """)

    conn.execute("""
        INSERT INTO stat_horse_distance_category
        SELECT
            rp.horse_id,
            CASE
                WHEN r.distance < 1200 THEN '短距離'
                WHEN r.distance < 1800 THEN 'マイル'
                WHEN r.distance < 2200 THEN '中距離'
                ELSE '長距離'
            END as distance_category,
            COUNT(*) as total_races,
            SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) as wins,
            CAST(SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) AS REAL) / COUNT(*) as win_rate,
            AVG(rp.finish_position) as avg_finish_position
        FROM race_performances rp
        JOIN races r ON rp.race_id = r.race_id
        WHERE rp.finish_position IS NOT NULL
        GROUP BY rp.horse_id, distance_category
        HAVING COUNT(*) >= 2
    """)

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM stat_horse_distance_category").fetchone()[0]
    print(f"  Inserted {count} rows\n")


def create_stat_gate_position(conn):
    """枠番統計テーブルを作成"""
    print("Creating stat_gate_position...")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS stat_gate_position (
            gate_number INTEGER NOT NULL,
            track_condition VARCHAR,
            distance_category VARCHAR,
            total_races INTEGER,
            wins INTEGER,
            win_rate REAL,
            PRIMARY KEY (gate_number, track_condition, distance_category)
        )
    """)

    conn.execute("""
        INSERT INTO stat_gate_position
        SELECT
            e.gate_number,
            r.track_condition,
            CASE
                WHEN r.distance < 1200 THEN '短距離'
                WHEN r.distance < 1800 THEN 'マイル'
                WHEN r.distance < 2200 THEN '中距離'
                ELSE '長距離'
            END as distance_category,
            COUNT(*) as total_races,
            SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) as wins,
            CAST(SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) AS REAL) / COUNT(*) as win_rate
        FROM entries e
        JOIN races r ON e.race_id = r.race_id
        JOIN race_performances rp ON e.entry_id = rp.entry_id
        WHERE rp.finish_position IS NOT NULL
        GROUP BY e.gate_number, r.track_condition, distance_category
    """)

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM stat_gate_position").fetchone()[0]
    print(f"  Inserted {count} rows\n")


def create_stat_horse_number(conn):
    """馬番統計テーブルを作成（オカルト検証用）"""
    print("Creating stat_horse_number...")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS stat_horse_number (
            horse_number INTEGER NOT NULL,
            total_races INTEGER,
            wins INTEGER,
            win_rate REAL,
            PRIMARY KEY (horse_number)
        )
    """)

    conn.execute("""
        INSERT INTO stat_horse_number
        SELECT
            e.horse_number,
            COUNT(*) as total_races,
            SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) as wins,
            CAST(SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) AS REAL) / COUNT(*) as win_rate
        FROM entries e
        JOIN race_performances rp ON e.entry_id = rp.entry_id
        WHERE rp.finish_position IS NOT NULL
        GROUP BY e.horse_number
        ORDER BY e.horse_number
    """)

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM stat_horse_number").fetchone()[0]
    print(f"  Inserted {count} rows\n")


def create_stat_track_distance_matrix(conn):
    """馬場×距離マトリックステーブルを作成"""
    print("Creating stat_track_distance_matrix...")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS stat_track_distance_matrix (
            track_condition VARCHAR NOT NULL,
            distance_category VARCHAR NOT NULL,
            total_races INTEGER,
            avg_trifecta_payout REAL,
            PRIMARY KEY (track_condition, distance_category)
        )
    """)

    conn.execute("""
        INSERT INTO stat_track_distance_matrix
        SELECT
            r.track_condition,
            CASE
                WHEN r.distance < 1200 THEN '短距離'
                WHEN r.distance < 1800 THEN 'マイル'
                WHEN r.distance < 2200 THEN '中距離'
                ELSE '長距離'
            END as distance_category,
            COUNT(DISTINCT r.race_id) as total_races,
            ROUND(AVG(CASE WHEN p.payout_type = 'trifecta' THEN p.payout ELSE NULL END), 0) as avg_trifecta_payout
        FROM races r
        LEFT JOIN payouts p ON r.race_id = p.race_id
        GROUP BY r.track_condition, distance_category
    """)

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM stat_track_distance_matrix").fetchone()[0]
    print(f"  Inserted {count} rows\n")


def create_stat_running_style(conn):
    """脚質統計テーブルを作成"""
    print("Creating stat_running_style...")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS stat_running_style (
            horse_id VARCHAR NOT NULL,
            avg_corner1_position REAL,
            avg_corner4_position REAL,
            position_change_avg REAL,
            total_races INTEGER,
            PRIMARY KEY (horse_id)
        )
    """)

    # コーナー通過順が数値として解釈可能な場合のみ集計
    conn.execute("""
        INSERT INTO stat_running_style
        SELECT
            horse_id,
            ROUND(AVG(CAST(corner_1_position AS REAL)), 2) as avg_corner1_position,
            ROUND(AVG(CAST(corner_4_position AS REAL)), 2) as avg_corner4_position,
            ROUND(AVG(CAST(corner_1_position AS REAL) - CAST(corner_4_position AS REAL)), 2) as position_change_avg,
            COUNT(*) as total_races
        FROM race_performances
        WHERE corner_1_position IS NOT NULL
          AND corner_4_position IS NOT NULL
          AND corner_1_position NOT LIKE '%-%'
          AND corner_4_position NOT LIKE '%-%'
          AND corner_1_position != ''
          AND corner_4_position != ''
        GROUP BY horse_id
        HAVING COUNT(*) >= 3
    """)

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM stat_running_style").fetchone()[0]
    print(f"  Inserted {count} rows\n")


def create_stat_last_3f_performance(conn):
    """上り3F統計テーブルを作成"""
    print("Creating stat_last_3f_performance...")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS stat_last_3f_performance (
            horse_id VARCHAR NOT NULL,
            avg_last_3f REAL,
            best_last_3f REAL,
            total_races INTEGER,
            PRIMARY KEY (horse_id)
        )
    """)

    conn.execute("""
        INSERT INTO stat_last_3f_performance
        SELECT
            horse_id,
            ROUND(AVG(CAST(last_3f AS REAL)), 2) as avg_last_3f,
            MIN(CAST(last_3f AS REAL)) as best_last_3f,
            COUNT(*) as total_races
        FROM race_performances
        WHERE last_3f IS NOT NULL
          AND last_3f NOT LIKE '%-%'
          AND last_3f != ''
          AND CAST(last_3f AS REAL) > 0
        GROUP BY horse_id
        HAVING COUNT(*) >= 3
    """)

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM stat_last_3f_performance").fetchone()[0]
    print(f"  Inserted {count} rows\n")


def create_stat_seasonal_performance(conn):
    """季節別成績統計テーブルを作成"""
    print("Creating stat_seasonal_performance...")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS stat_seasonal_performance (
            entity_type VARCHAR NOT NULL,
            entity_id VARCHAR NOT NULL,
            season VARCHAR NOT NULL,
            total_races INTEGER,
            wins INTEGER,
            win_rate REAL,
            PRIMARY KEY (entity_type, entity_id, season)
        )
    """)

    # 馬の季節別成績
    conn.execute("""
        INSERT INTO stat_seasonal_performance
        SELECT
            'horse' as entity_type,
            rp.horse_id as entity_id,
            CASE
                WHEN CAST(strftime('%m', r.date) AS INTEGER) IN (3, 4, 5) THEN 'spring'
                WHEN CAST(strftime('%m', r.date) AS INTEGER) IN (6, 7, 8) THEN 'summer'
                WHEN CAST(strftime('%m', r.date) AS INTEGER) IN (9, 10, 11) THEN 'autumn'
                ELSE 'winter'
            END as season,
            COUNT(*) as total_races,
            SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) as wins,
            CAST(SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) AS REAL) / COUNT(*) as win_rate
        FROM race_performances rp
        JOIN races r ON rp.race_id = r.race_id
        WHERE rp.finish_position IS NOT NULL
        GROUP BY rp.horse_id, season
        HAVING COUNT(*) >= 2
    """)

    # 騎手の季節別成績
    conn.execute("""
        INSERT INTO stat_seasonal_performance
        SELECT
            'jockey' as entity_type,
            e.jockey_id as entity_id,
            CASE
                WHEN CAST(strftime('%m', r.date) AS INTEGER) IN (3, 4, 5) THEN 'spring'
                WHEN CAST(strftime('%m', r.date) AS INTEGER) IN (6, 7, 8) THEN 'summer'
                WHEN CAST(strftime('%m', r.date) AS INTEGER) IN (9, 10, 11) THEN 'autumn'
                ELSE 'winter'
            END as season,
            COUNT(*) as total_races,
            SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) as wins,
            CAST(SUM(CASE WHEN rp.finish_position = 1 THEN 1 ELSE 0 END) AS REAL) / COUNT(*) as win_rate
        FROM entries e
        JOIN races r ON e.race_id = r.race_id
        JOIN race_performances rp ON e.entry_id = rp.entry_id
        WHERE rp.finish_position IS NOT NULL
        GROUP BY e.jockey_id, season
        HAVING COUNT(*) >= 5
    """)

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM stat_seasonal_performance").fetchone()[0]
    print(f"  Inserted {count} rows\n")


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(description='統計テーブル構築スクリプト')
    parser.add_argument('--drop', action='store_true', help='既存の統計テーブルを削除してから再構築')
    args = parser.parse_args()

    print("=" * 60)
    print("統計テーブル構築")
    print("=" * 60)
    print()

    conn = get_connection()

    try:
        if args.drop:
            drop_stats_tables(conn)

        # 累積成績テーブル (3個)
        create_stat_horse_cumulative(conn)
        create_stat_jockey_cumulative(conn)
        create_stat_trainer_cumulative(conn)

        # 組み合わせ統計 (3個)
        create_stat_horse_jockey_combo(conn)
        create_stat_horse_trainer_combo(conn)
        create_stat_jockey_trainer_combo(conn)

        # レース条件別統計 (3個)
        create_stat_horse_track_condition(conn)
        create_stat_horse_distance_category(conn)
        create_stat_track_distance_matrix(conn)

        # 枠番・馬番統計 (2個)
        create_stat_gate_position(conn)
        create_stat_horse_number(conn)

        # 人気別統計 (1個)
        create_stat_popularity_performance(conn)

        # レース展開・脚質統計 (1個)
        create_stat_running_style(conn)

        # 時間統計 (1個)
        create_stat_last_3f_performance(conn)

        # 季節統計 (1個)
        create_stat_seasonal_performance(conn)

        print("=" * 60)
        print("統計テーブル構築完了 - 15個のテーブルを作成")
        print("=" * 60)

    except Exception as e:
        print(f"\nError: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
