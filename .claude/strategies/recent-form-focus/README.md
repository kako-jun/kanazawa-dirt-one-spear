# 作戦: 直近成績重視型 (Recent Form Focus)

**ID**: `recent-form-focus`
**バージョン**: 1.0.0
**ステータス**: 計画中
**優先度**: 中

## 概要

**「今、調子が良い」馬を見つける**作戦。

累積統計は過去全体の平均だが、馬のコンディションは変動する。直近の成績（フォーム）を重視することで、現在の実力を正確に捉える。

## 仮説

- **調子には波がある**: ピーク期と低迷期が存在
- **直近が重要**: 1年前の成績より先週の成績が価値が高い
- **トレンドを捉える**: 成績向上中か、下降中かが重要
- **時間的減衰**: 古いデータの重みを下げる（Exponential Decay）

## 時間的減衰の概念

```
累積勝率（全期間平均）:
  2020年: 1勝/10戦 = 10%
  2021年: 2勝/10戦 = 20%
  2022年: 0勝/10戦 = 0%
  2023年: 3勝/10戦 = 30%
  → 累積: 6勝/40戦 = 15%

時間減衰勝率（直近重視）:
  2020年: weight=0.1
  2021年: weight=0.3
  2022年: weight=0.7
  2023年: weight=1.0
  → 加重: 約25%（直近を重視！）
```

## アルゴリズム

### 1. 時間的減衰重み付け

```python
import numpy as np

def calculate_recent_win_rate(races, lambda_decay=0.01):
    """
    時間的減衰を考慮した勝率

    Args:
        races: レース履歴（新しい順）
        lambda_decay: 減衰率（大きいほど直近重視）

    Returns:
        recent_win_rate
    """
    weights = []
    wins = []

    for i, race in enumerate(races):
        days_ago = (today - race['date']).days
        weight = np.exp(-lambda_decay * days_ago)

        weights.append(weight)
        wins.append(race['win'] * weight)

    recent_win_rate = sum(wins) / sum(weights)
    return recent_win_rate
```

### 2. 連勝・連敗検出

```python
def detect_streak(recent_races):
    """
    連勝・連敗を検出

    Returns:
        streak_type: 'winning' | 'losing' | 'none'
        streak_count: 連続数
    """
    if len(recent_races) < 2:
        return 'none', 0

    # 直近3戦の結果
    results = [r['finish_position'] for r in recent_races[:3]]

    # 連勝チェック（3着以内）
    if all(r <= 3 for r in results):
        return 'winning', len(results)

    # 連敗チェック（5着以下）
    if all(r >= 5 for r in results):
        return 'losing', len(results)

    return 'none', 0
```

### 3. トレンド検出

```python
def detect_improving_trend(recent_races):
    """
    成績向上傾向を検出

    Returns:
        is_improving: True/False
    """
    if len(recent_races) < 4:
        return False

    # 直近4戦を2つに分割
    older = recent_races[2:4]  # 3-4戦前
    newer = recent_races[0:2]  # 1-2戦前

    avg_older = np.mean([r['finish_position'] for r in older])
    avg_newer = np.mean([r['finish_position'] for r in newer])

    # 平均着順が改善していればTrue
    return avg_newer < avg_older
```

## 実装

### スクリプト

1. **`analysis/recent_form_focus/calculate_recent_stats.py`**
   - 直近30/60/90日の成績計算

2. **`analysis/recent_form_focus/detect_streaks.py`**
   - 連勝・連敗の検出

3. **`analysis/recent_form_focus/exponential_weighting.py`**
   - 時間的減衰重み付け

4. **`analysis/recent_form_focus/train_model.py`**
   - LightGBM訓練（直近特徴量込み）

## 評価指標

### 的中率
```
目標: 6%以上
```

### 連勝馬の的中率
```
連勝中の馬の予測精度: 80%以上
```

### Feature Importance
```
recent_form特徴量が上位に入るか
```

## 次のステップ

- [ ] 直近成績計算ロジック実装
- [ ] 最適なλ（減衰率）探索
- [ ] 連勝・連敗検出
- [ ] basic-win-probとの比較

---

**作成日**: 2025-11-16
**最終更新**: 2025-11-16
