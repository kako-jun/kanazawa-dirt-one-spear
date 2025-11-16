# 作戦: 3連単パターン学習型 (Trifecta Pattern Learning)

**ID**: `trifecta-pattern-learning`
**バージョン**: 1.0.0
**ステータス**: 計画中
**優先度**: 高

## 概要

**「1着予測×3」ではなく、3連単の『型』を直接学習する**革新的アプローチ。

「1番人気-3番人気-5番人気」「逃げ馬-差し馬-追込馬」など、3連単には特定のパターンが存在する。個々の馬の実力ではなく、**レース全体の構図・組み合わせパターン**を予測することで3連単に特化した精度を実現。

## 仮説

- **3連単には『型』がある**: ランダムではなく、再現性のあるパターンが存在
- **人気の組み合わせに偏りがある**: 例えば「1-2-3」より「1-3-5」が多い
- **脚質の組み合わせに傾向**: 「逃げ-先行-差し」など
- **万馬券には法則性**: オッズが高いが実は確率も高い組み合わせが存在
- **人間の盲点**: 見落とされがちな組み合わせをAIが発見

## 3連単パターンの例

### 人気パターン

```
過去8,733レースの分析結果（仮）:

「1-2-3番人気」: 12% （順当決着）
「1-2-4番人気」: 8%
「1-3-5番人気」: 7%  ← 意外と多い！
「1-4-7番人気」: 5%  ← 万馬券だが頻出
「2-1-3番人気」: 6%
「2-3-5番人気」: 4%  ← 中穴狙い
```

### 脚質パターン

```
「逃げ-先行-差し」: 18%
「逃げ-差し-追込」: 12%
「先行-差し-差し」: 15%
「差し-差し-追込」: 10%（スローペース時）
```

### 万馬券パターン

```
配当10,000円以上の3連単パターン分析:

人気パターン:
「1-4-7」: 配当平均12,000円、出現率5% ← 狙い目！
「1-5-8」: 配当平均18,000円、出現率3%
「2-5-7」: 配当平均15,000円、出現率4%

条件パターン:
- 稍重×1400m → 「1-3-6」が多い
- 重×1900m → 「2-4-5」が多い
```

## アルゴリズム

### 1. パターン抽出

```python
def extract_trifecta_patterns(races):
    """
    過去の3連単パターンを抽出
    """
    patterns = []

    for race in races:
        # 1-2-3着の人気順位パターン
        top3_horses = race.get_top3()
        popularity_pattern = tuple([h.popularity for h in top3_horses])

        # 脚質パターン
        running_style_pattern = tuple([h.running_style for h in top3_horses])

        # 配当
        payout = race.trifecta_payout

        patterns.append({
            'race_conditions': race.get_conditions(),
            'popularity_pattern': popularity_pattern,
            'running_style_pattern': running_style_pattern,
            'payout': payout,
        })

    return patterns
```

### 2. パターン頻度分析

```python
from collections import Counter

def analyze_pattern_frequency(patterns):
    """
    パターンの頻度と配当を分析
    """
    popularity_counter = Counter([p['popularity_pattern'] for p in patterns])

    print("頻出人気パターン トップ20:")
    for pattern, count in popularity_counter.most_common(20):
        avg_payout = calculate_avg_payout(patterns, pattern)
        frequency = count / len(patterns)

        print(f"{pattern}: {frequency:.1%} 平均配当{avg_payout:,}円")
```

### 3. オッズバイアス検出（万馬券狙い）

```python
def find_undervalued_patterns(patterns):
    """
    オッズの割に確率が高いパターンを発見

    期待値 = 出現確率 × 配当 - 100
    """
    pattern_stats = {}

    for pattern_id, pattern_group in group_by_pattern(patterns):
        frequency = len(pattern_group) / len(patterns)
        avg_payout = np.mean([p['payout'] for p in pattern_group])

        ev = frequency * avg_payout - 100

        pattern_stats[pattern_id] = {
            'frequency': frequency,
            'avg_payout': avg_payout,
            'ev': ev,
        }

    # 期待値が高い順にソート
    sorted_patterns = sorted(pattern_stats.items(), key=lambda x: x[1]['ev'], reverse=True)

    print("期待値が高いパターン（万馬券狙い）:")
    for pattern, stats in sorted_patterns[:20]:
        print(f"{pattern}: EV={stats['ev']:.0f}円 確率={stats['frequency']:.1%} 配当={stats['avg_payout']:,}円")

    return sorted_patterns
```

### 4. パターン予測

```python
def predict_pattern(race_conditions, pattern_classifier):
    """
    レース条件からパターンを予測
    """
    # レース条件を特徴量化
    features = extract_race_features(race_conditions)

    # パターン分類器で予測
    predicted_pattern = pattern_classifier.predict(features)

    # 例: (1, 3, 5) = 1番人気-3番人気-5番人気

    # 実際の馬に当てはめ
    horses = race_conditions.get_horses()
    first = horses.get_by_popularity(predicted_pattern[0])
    second = horses.get_by_popularity(predicted_pattern[1])
    third = horses.get_by_popularity(predicted_pattern[2])

    return [first, second, third]
```

## 実装

### スクリプト

1. **`analysis/trifecta_pattern_learning/extract_patterns.py`**
   - 過去の3連単パターン抽出

2. **`analysis/trifecta_pattern_learning/pattern_frequency.py`**
   - パターン頻度分析、万馬券パターン特定

3. **`analysis/trifecta_pattern_learning/train_pattern_classifier.py`**
   - パターン分類器訓練（LightGBM）

4. **`analysis/trifecta_pattern_learning/predict_pattern.py`**
   - パターン予測

### 新規テーブル

```sql
CREATE TABLE trifecta_patterns (
  id INTEGER PRIMARY KEY,
  race_id INTEGER,
  popularity_pattern VARCHAR,  -- 例: "1-3-5"
  running_style_pattern VARCHAR,  -- 例: "逃げ-差し-追込"
  payout INTEGER,
  is_万馬券 BOOLEAN,  -- 10,000円以上
  pattern_frequency REAL,  -- このパターンの全体出現率
  ev REAL,  -- 期待値
  created_at TIMESTAMP
);
```

## 評価指標

### パターン予測精度
```
目標: 30%以上（336通りの3連単のうち、パターンは20-30種類に絞られる）
```

### 3連単的中率
```
目標: 7%以上（basic-win-probの1.5倍）
```

### 万馬券的中率
```
配当10,000円以上の的中率: 2%以上
```

### 期待値
```
長期的な期待値: プラス
```

## 万馬券狙いの戦略

### 高配当×高確率パターン

過去データから以下のようなパターンが見つかる可能性：

```
パターン「1-4-7」:
- 出現確率: 5%
- 平均配当: 12,000円
- 期待値: 0.05 × 12,000 - 100 = +500円 ← 狙い目！

パターン「1-2-3」:
- 出現確率: 12%
- 平均配当: 800円
- 期待値: 0.12 × 800 - 100 = -4円 ← 期待値マイナス
```

## 次のステップ

- [ ] 過去の3連単パターン抽出
- [ ] 頻出パターンの特定
- [ ] 万馬券パターンの分析
- [ ] 期待値計算
- [ ] パターン分類器実装
- [ ] basic-win-probとの比較

---

**作成日**: 2025-11-16
**最終更新**: 2025-11-16
