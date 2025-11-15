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

    # データ投入
    conn.execute("""
        INSERT INTO stat_horse_cumulative
        SELECT
            horse_id,
            race_date as as_of_date,
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
        SELECT
            jockey_id,
            race_date as as_of_date,
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
        SELECT
            trainer_id,
            race_date as as_of_date,
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

        # 累積成績テーブル
        create_stat_horse_cumulative(conn)
        create_stat_jockey_cumulative(conn)
        create_stat_trainer_cumulative(conn)

        # 組み合わせ統計
        create_stat_horse_jockey_combo(conn)

        # 条件別統計
        create_stat_horse_track_condition(conn)

        # 人気別統計
        create_stat_popularity_performance(conn)

        print("=" * 60)
        print("統計テーブル構築完了")
        print("=" * 60)

    except Exception as e:
        print(f"\nError: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
