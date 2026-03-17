# 統計テーブル設計

## 命名規則
- プリフィックス: `stat_`
- 基本テーブルと明確に区別
- 削除/再構築が容易: `DROP TABLE IF EXISTS stat_%`

---

## 1. 累積成績テーブル

### stat_horse_cumulative
**目的**: 馬の累積成績（日付ごと）

```sql
CREATE TABLE stat_horse_cumulative (
    horse_id VARCHAR NOT NULL,
    as_of_date DATE NOT NULL,
    total_races INTEGER,
    wins INTEGER,
    places INTEGER,
    win_rate REAL,
    place_rate REAL,
    avg_finish_position REAL,
    avg_margin REAL,
    days_since_last_race INTEGER,
    rest_days_avg REAL,
    PRIMARY KEY (horse_id, as_of_date)
);
CREATE INDEX idx_horse_cum_date ON stat_horse_cumulative(as_of_date);
```

**活用案**:
- 成長曲線の分析
- 休養効果の検証
- ピーク期の検出

---

### stat_jockey_cumulative
**目的**: 騎手の累積成績

```sql
CREATE TABLE stat_jockey_cumulative (
    jockey_id VARCHAR NOT NULL,
    as_of_date DATE NOT NULL,
    total_races INTEGER,
    wins INTEGER,
    places INTEGER,
    win_rate REAL,
    place_rate REAL,
    avg_finish_position REAL,
    total_prize_money INTEGER,
    PRIMARY KEY (jockey_id, as_of_date)
);
CREATE INDEX idx_jockey_cum_date ON stat_jockey_cumulative(as_of_date);
```

**活用案**:
- 好調・不調期の検出
- 経験値の影響分析

---

### stat_trainer_cumulative
**目的**: 調教師の累積成績

```sql
CREATE TABLE stat_trainer_cumulative (
    trainer_id VARCHAR NOT NULL,
    as_of_date DATE NOT NULL,
    total_races INTEGER,
    wins INTEGER,
    places INTEGER,
    win_rate REAL,
    place_rate REAL,
    PRIMARY KEY (trainer_id, as_of_date)
);
CREATE INDEX idx_trainer_cum_date ON stat_trainer_cumulative(as_of_date);
```

---

## 2. 組み合わせ統計

### stat_horse_jockey_combo
**目的**: 馬×騎手の相性統計

```sql
CREATE TABLE stat_horse_jockey_combo (
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
);
```

**活用案**:
- 相性の良い組み合わせ検出
- 初コンビの不利を考慮

---

### stat_horse_trainer_combo
**目的**: 馬×調教師の統計

```sql
CREATE TABLE stat_horse_trainer_combo (
    horse_id VARCHAR NOT NULL,
    trainer_id VARCHAR NOT NULL,
    total_races INTEGER,
    wins INTEGER,
    places INTEGER,
    win_rate REAL,
    PRIMARY KEY (horse_id, trainer_id)
);
```

---

### stat_jockey_trainer_combo
**目的**: 騎手×調教師の連携統計

```sql
CREATE TABLE stat_jockey_trainer_combo (
    jockey_id VARCHAR NOT NULL,
    trainer_id VARCHAR NOT NULL,
    total_races INTEGER,
    wins INTEGER,
    places INTEGER,
    win_rate REAL,
    PRIMARY KEY (jockey_id, trainer_id)
);
```

**活用案**:
- 厩舎と騎手の連携度評価

---

## 3. レース条件別統計

### stat_track_distance_matrix
**目的**: 馬場×距離の統計マトリックス

```sql
CREATE TABLE stat_track_distance_matrix (
    track_condition VARCHAR NOT NULL,
    distance_category VARCHAR NOT NULL,
    total_races INTEGER,
    avg_win_rate REAL,
    avg_trifecta_payout REAL,
    PRIMARY KEY (track_condition, distance_category)
);
```

**活用案**:
- 荒れやすい条件の特定
- 配当期待値の推定

---

### stat_horse_track_condition
**目的**: 馬ごとの馬場適性

```sql
CREATE TABLE stat_horse_track_condition (
    horse_id VARCHAR NOT NULL,
    track_condition VARCHAR NOT NULL,
    total_races INTEGER,
    wins INTEGER,
    win_rate REAL,
    PRIMARY KEY (horse_id, track_condition)
);
```

**活用案**:
- 重馬場巧者の発見
- 馬場替わり時の予想精度向上

---

### stat_horse_distance_category
**目的**: 馬ごとの距離適性

```sql
CREATE TABLE stat_horse_distance_category (
    horse_id VARCHAR NOT NULL,
    distance_category VARCHAR NOT NULL,
    total_races INTEGER,
    wins INTEGER,
    win_rate REAL,
    avg_finish_position REAL,
    PRIMARY KEY (horse_id, distance_category)
);
```

**活用案**:
- 距離延長・短縮の影響分析

---

## 4. 枠番・馬番統計

### stat_gate_position
**目的**: 枠番別の成績

```sql
CREATE TABLE stat_gate_position (
    gate_number INTEGER NOT NULL,
    track_condition VARCHAR,
    distance_category VARCHAR,
    total_races INTEGER,
    wins INTEGER,
    win_rate REAL,
    PRIMARY KEY (gate_number, track_condition, distance_category)
);
```

**活用案**:
- 有利な枠の特定
- 条件による枠の有利不利

---

### stat_horse_number
**目的**: 馬番別の成績（ジンクス検証）

```sql
CREATE TABLE stat_horse_number (
    horse_number INTEGER NOT NULL,
    total_races INTEGER,
    wins INTEGER,
    win_rate REAL,
    PRIMARY KEY (horse_number)
);
```

**活用案**:
- オカルト検証
- 馬番による偏りの有無確認

---

## 5. 人気別統計

### stat_popularity_performance
**目的**: 人気ランク別の成績

```sql
CREATE TABLE stat_popularity_performance (
    popularity INTEGER NOT NULL,
    total_races INTEGER,
    wins INTEGER,
    places INTEGER,
    win_rate REAL,
    place_rate REAL,
    avg_payout REAL,
    PRIMARY KEY (popularity)
);
```

**活用案**:
- 人気と実力の乖離分析
- オッズバリュー分析

---

## 6. オッズバイアス分析

### stat_odds_bias
**目的**: 人気と実際の結果の乖離

```sql
CREATE TABLE stat_odds_bias (
    horse_id VARCHAR NOT NULL,
    expected_win_rate REAL,  -- オッズから計算
    actual_win_rate REAL,    -- 実際の勝率
    bias REAL,               -- 乖離度
    total_races INTEGER,
    over_performs BOOLEAN,   -- 過小評価されているか
    PRIMARY KEY (horse_id)
);
```

**活用案**:
- 穴馬発見（過小評価馬）
- 人気馬除外（過大評価馬）

---

## 7. レース展開・脚質統計

### stat_running_style
**目的**: 馬の脚質判定

```sql
CREATE TABLE stat_running_style (
    horse_id VARCHAR NOT NULL,
    style VARCHAR,  -- 'front_runner', 'stalker', 'closer'
    avg_corner1_position REAL,
    avg_corner4_position REAL,
    position_change_avg REAL,
    total_races INTEGER,
    PRIMARY KEY (horse_id)
);
```

**活用案**:
- 展開予想
- 逃げ馬不在のレースで先行有利

---

### stat_pace_pattern
**目的**: レース展開パターン

```sql
CREATE TABLE stat_pace_pattern (
    race_id VARCHAR NOT NULL,
    pace VARCHAR,  -- 'slow', 'medium', 'fast'
    avg_corner1_leaders REAL,
    position_changes_avg REAL,
    PRIMARY KEY (race_id)
);
```

**活用案**:
- スローペース時の差し馬狙い
- ハイペース時の先行馬除外

---

## 8. 時間統計

### stat_last_3f_performance
**目的**: 上り3Fタイム統計

```sql
CREATE TABLE stat_last_3f_performance (
    horse_id VARCHAR NOT NULL,
    avg_last_3f REAL,
    best_last_3f REAL,
    last_3f_variance REAL,
    total_races INTEGER,
    PRIMARY KEY (horse_id)
);
```

**活用案**:
- 末脚の強さ評価
- 瞬発力重視レースで有利

---

### stat_rest_days_effect
**目的**: 休養期間の影響分析

```sql
CREATE TABLE stat_rest_days_effect (
    rest_days_category VARCHAR NOT NULL,  -- '0-7', '8-14', '15-30', '31-60', '61+'
    total_races INTEGER,
    wins INTEGER,
    win_rate REAL,
    avg_finish_position REAL,
    PRIMARY KEY (rest_days_category)
);
```

**活用案**:
- 適度な休養期間の特定
- 連闘・長期休養の影響評価

---

## 9. 季節・時期統計

### stat_seasonal_performance
**目的**: 季節・月別成績

```sql
CREATE TABLE stat_seasonal_performance (
    entity_type VARCHAR NOT NULL,  -- 'horse', 'jockey', 'trainer'
    entity_id VARCHAR NOT NULL,
    season VARCHAR NOT NULL,  -- 'spring', 'summer', 'autumn', 'winter'
    month INTEGER,
    total_races INTEGER,
    wins INTEGER,
    win_rate REAL,
    PRIMARY KEY (entity_type, entity_id, season)
);
```

**活用案**:
- 季節適性の発見
- 夏場に強い馬の特定

---

## 10. ヘッドトゥヘッド統計

### stat_head_to_head
**目的**: 馬同士の対戦成績

```sql
CREATE TABLE stat_head_to_head (
    horse_a_id VARCHAR NOT NULL,
    horse_b_id VARCHAR NOT NULL,
    total_encounters INTEGER,
    horse_a_wins INTEGER,
    horse_b_wins INTEGER,
    PRIMARY KEY (horse_a_id, horse_b_id)
);
```

**活用案**:
- 相性の良い・悪い相手の特定

---

## 構築スクリプト

すべてのテーブルを構築: `backend/build_stats_tables.py`
削除: `backend/drop_stats_tables.py`

## 期待される作戦アイデア

これらのテーブルを組み合わせることで：

1. **相性重視作戦**: horse_jockey_combo + jockey_trainer_combo
2. **条件スペシャリスト**: track_condition + distance_category
3. **穴馬ハンター**: odds_bias + popularity_performance
4. **展開予想型**: running_style + pace_pattern
5. **時期限定**: seasonal_performance + rest_days_effect
6. **脚質マッチング**: running_style + last_3f_performance

---

**最終更新**: 2025-11-15
