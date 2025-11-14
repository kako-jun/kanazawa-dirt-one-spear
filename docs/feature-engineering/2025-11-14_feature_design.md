# 特徴量設計 - 金沢競馬AI予想システム

**作成日**: 2025-11-14
**モデル**: LightGBM Ranker（オッズなし版）

---

## 設計方針

### 1. オッズを使わない理由

`.claude/analysis/prediction.md`の哲学に基づき、まず**オッズを完全に無視したモデル**を構築する。

**目的**:
- 人間の集団心理バイアスに影響されない純粋なAI判断
- 過小評価されている馬を発見できる可能性
- オッズあり/なしモデルの比較実験の基盤

**次フェーズ**: オッズを特徴量に含めたモデルBを構築し、両者を比較

---

## 特徴量カテゴリー

### A. レース基本特徴量（8特徴）

| 特徴量名 | 型 | 説明 | 欠損処理 |
|---------|-----|------|----------|
| `distance` | int | レース距離（m） | 欠損なし |
| `track_condition_encoded` | int | 馬場状態（良=0, 稍重=1, 重=2, 不良=3） | 欠損なし |
| `weather_encoded` | int | 天候（晴=0, 曇=1, 雨=2, 雪=3） | 欠損なし |
| `race_class_encoded` | int | レースクラス（C1, C2等） | "unknown"=0 |
| `month` | int | 月（4-11） | 欠損なし |
| `day_of_week` | int | 曜日（月=0〜日=6） | 欠損なし |
| `race_number` | int | レース番号（1-12） | 欠損なし |
| `num_horses` | int | 出走頭数 | 欠損なし |

### B. 馬の基本特徴量（6特徴）

| 特徴量名 | 型 | 説明 | 欠損処理 |
|---------|-----|------|----------|
| `horse_number` | int | 馬番 | 欠損なし |
| `gate_number` | int | 枠番 | 欠損なし |
| `horse_age` | int | 馬齢 | 中央値 |
| `horse_gender_encoded` | int | 性別（牡=0, 牝=1, 騙=2, unknown=3） | unknown=3 |
| `horse_weight` | float | 馬体重（kg） | 中央値 |
| `weight_diff_value` | float | 馬体重増減（kg） | 0 |

### C. 騎手特徴量（3特徴）

| 特徴量名 | 型 | 説明 | 欠損処理 |
|---------|-----|------|----------|
| `jockey_id_encoded` | int | 騎手ID（Label Encoding） | 欠損なし |
| `weight_carried` | float | 斤量（kg） | 欠損なし |
| `jockey_experience` | int | 騎手の経験年数（初騎乗年からの経過） | 0 |

### D. 過去成績特徴量（馬）（10特徴）

各馬の過去成績を集計した特徴量。**当該レースより前のデータのみ使用**（時系列リーク防止）。

| 特徴量名 | 型 | 説明 | 欠損処理 |
|---------|-----|------|----------|
| `horse_total_races` | int | 総出走回数 | 0 |
| `horse_win_rate` | float | 勝率（1着/総出走） | 0.0 |
| `horse_place_rate` | float | 連対率（1-2着/総出走） | 0.0 |
| `horse_show_rate` | float | 複勝率（1-3着/総出走） | 0.0 |
| `horse_avg_finish` | float | 平均着順 | 出走頭数の平均 |
| `horse_win_rate_distance` | float | 同距離での勝率 | 0.0 |
| `horse_win_rate_track_bad` | float | 不良馬場での勝率 | 0.0 |
| `horse_recent_5_avg_finish` | float | 直近5走の平均着順 | 0.0 |
| `horse_days_since_last_race` | int | 前走からの日数 | 999 |
| `horse_best_time` | float | ベストタイム（秒） | 999.9 |

### E. 過去成績特徴量（騎手）（8特徴）

各騎手の過去成績を集計。**当該レースより前のデータのみ使用**。

| 特徴量名 | 型 | 説明 | 欠損処理 |
|---------|-----|------|----------|
| `jockey_total_races` | int | 総騎乗回数 | 0 |
| `jockey_win_rate` | float | 勝率 | 0.0 |
| `jockey_place_rate` | float | 連対率 | 0.0 |
| `jockey_show_rate` | float | 複勝率 | 0.0 |
| `jockey_win_rate_distance` | float | 同距離での勝率 | 0.0 |
| `jockey_win_rate_track_bad` | float | 不良馬場での勝率 | 0.0 |
| `jockey_recent_10_avg_finish` | float | 直近10騎乗の平均着順 | 0.0 |
| `jockey_win_rate_with_horse` | float | この馬との勝率 | 0.0 |

### F. 相対的特徴量（6特徴）

レース内での相対的な位置を表す特徴量。

| 特徴量名 | 型 | 説明 | 生成方法 |
|---------|-----|------|----------|
| `horse_weight_rank` | int | 馬体重順位（1=最重） | レース内ランキング |
| `jockey_win_rate_rank` | int | 騎手勝率順位（1=最高勝率） | レース内ランキング |
| `horse_win_rate_rank` | int | 馬勝率順位 | レース内ランキング |
| `weight_carried_rank` | int | 斤量順位（1=最重） | レース内ランキング |
| `horse_experience_rank` | int | 出走経験順位（1=最多経験） | レース内ランキング |
| `normalized_horse_number` | float | 正規化馬番（馬番/出走頭数） | 0.0-1.0 |

---

## 実装計画

### Phase 1: 基本特徴量の実装

```python
# analysis/feature_engineering.py

import pandas as pd
import numpy as np
from pathlib import Path
import sqlite3
from datetime import datetime

class FeatureEngineer:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)

    def extract_race_basic_features(self, race_df):
        """レース基本特徴量を抽出"""
        pass

    def extract_horse_basic_features(self, entry_df):
        """馬基本特徴量を抽出"""
        pass

    def calculate_horse_stats(self, horse_id, up_to_date):
        """指定日時点での馬の過去成績を計算"""
        pass

    def calculate_jockey_stats(self, jockey_id, up_to_date):
        """指定日時点での騎手の過去成績を計算"""
        pass

    def create_dataset(self, start_date=None, end_date=None):
        """学習/評価用データセットを作成"""
        pass
```

### Phase 2: 時系列リークの防止

**重要**: 過去成績特徴量は必ず「当該レースより前」のデータのみを使用。

```python
def calculate_horse_stats(self, horse_id, up_to_date):
    query = """
    SELECT * FROM entries e
    JOIN races r ON e.race_id = r.race_id
    JOIN results res ON r.race_id = res.race_id
    WHERE e.horse_id = ? AND r.date < ?
    ORDER BY r.date
    """
    # 当該レースより前のデータのみ取得
    df = pd.read_sql_query(query, self.conn, params=[horse_id, up_to_date])
    # 統計量を計算
    return stats
```

### Phase 3: 欠損値処理

1. **馬体重**: 中央値で補完（450kg程度）
2. **性別**: "unknown"カテゴリを追加
3. **過去成績**: 0埋め（新馬・新人）

### Phase 4: カテゴリカル変数のエンコーディング

- **順序あり**: track_condition（良 < 稍重 < 重 < 不良）
- **順序なし**: jockey_id（Label Encoding）

---

## 特徴量の優先度

### 最優先（必須）

- [x] レース基本情報（距離、馬場、天候）
- [x] 馬番・枠番
- [x] 騎手ID
- [x] 馬体重・斤量

### 高優先

- [ ] 馬の過去成績（勝率、連対率、複勝率）
- [ ] 騎手の過去成績
- [ ] 直近成績（Recent N走）

### 中優先

- [ ] 距離適性（同距離での成績）
- [ ] 馬場適性（悪馬場での成績）
- [ ] 馬×騎手の相性

### 低優先（Phase 2以降）

- [ ] 血統特徴量
- [ ] 調教師特徴量
- [ ] レース間隔の統計量

---

## データセット分割戦略

時系列クロスバリデーションを使用（`.claude/analysis/prediction.md`参照）。

### TimeSeriesSplit方式

```
2015-2019: Train | 2020: Val
2015-2020: Train | 2021: Val
2015-2021: Train | 2022: Val
2015-2022: Train | 2023: Val
2015-2023: Train | 2024: Val
```

**メリット**:
- 未来のデータが学習に混入しない
- 実運用に近い評価
- 時系列トレンドの変化を捉えられる

---

## 評価指標

### 1. 順位予測精度

- **NDCG@3**: 上位3頭の予測精度
- **MRR**: Mean Reciprocal Rank（1着馬が何位に予測されたか）
- **Precision@3**: 上位3頭のうち実際に1-3着に入った馬の割合

### 2. 的中率

- **3連単的中率**: AI予想1-2-3着が実際の結果と一致
- **3連複的中率**: 順不同で上位3頭を当てる
- **馬連的中率**: 上位2頭を当てる

### 3. 回収率（配当データ取得後）

- **単純回収率**: 払戻/購入金額
- **的中時平均配当**: 当たった時の平均払戻額

---

## 次のステップ

1. [ ] `analysis/feature_engineering.py`の実装
2. [ ] 基本特徴量の抽出テスト
3. [ ] 過去成績特徴量の時系列計算
4. [ ] データセットの生成とCSV保存
5. [ ] 特徴量の分布確認・可視化

---

**総特徴量数**: 約41次元

**データサイズ見積もり**:
- 79,283エントリー × 41次元 = 約3.2M要素
- メモリ消費: 約25MB（float32の場合）
- 処理時間: 数分程度（過去成績計算が重い）

---

**作成者**: Claude
**参考ドキュメント**: `.claude/analysis/prediction.md`, `.claude/analysis/analysis.md`
