# 作戦: アンサンブル統合型 (Ensemble Hybrid)

**ID**: `ensemble-hybrid`
**バージョン**: 1.0.0
**ステータス**: 計画中
**優先度**: 高

## 概要

**複数の作戦を組み合わせて最強の予測を作る**統合型アプローチ。

単一の作戦には必ず弱点があるが、異なる視点を持つ複数の作戦を組み合わせることで、互いの弱点を補完し、安定性と精度を同時に向上させる。

## 仮説

- **集合知は個より優れる**: Wisdom of Crowds
- **多様性が重要**: 異なる手法を組み合わせることでノイズを平滑化
- **弱点の補完**: ある作戦が苦手な条件を別の作戦がカバー
- **スタッキングで最適化**: メタ学習により最適な統合方法を自動発見

## アンサンブル学習の原理

```
単一モデル:
  精度: 70%
  弱点: 特定条件で大外れ

アンサンブル:
  モデルA: 70%（基本統計重視）
  モデルB: 68%（順位学習）
  モデルC: 65%（期待値重視）
  ↓ 統合
  精度: 75%（+5%向上！）
  安定性: 高（分散減少）
```

## 統合手法

### 1. Voting（投票）

**Hard Voting（多数決）**
```python
# 各作戦の1着予測
basic_win_prob → 馬A
learning_to_rank → 馬A
odds_value_hunter → 馬C
combo_affinity → 馬A

# 多数決
→ 馬A（3票）を1着に選択
```

**Soft Voting（確率平均）**
```python
# 各作戦の予測確率
basic_win_prob: 馬A=0.25, 馬B=0.18
learning_to_rank: 馬A=0.22, 馬B=0.20
odds_value_hunter: 馬A=0.15, 馬C=0.30

# 平均スコア
馬A: (0.25 + 0.22 + 0.15) / 3 = 0.21
馬B: (0.18 + 0.20 + 0.08) / 3 = 0.15
馬C: (0.10 + 0.12 + 0.30) / 3 = 0.17

# ソート
→ 馬A, 馬C, 馬B
```

### 2. Weighted Ensemble（重み付き統合）

性能が良い作戦の予測を重視：

```python
# 各作戦の性能（検証データ）
basic_win_prob: accuracy=0.40
learning_to_rank: accuracy=0.45
odds_value_hunter: accuracy=0.30

# 重み計算
total = 0.40 + 0.45 + 0.30 = 1.15
w1 = 0.40 / 1.15 = 0.35
w2 = 0.45 / 1.15 = 0.39
w3 = 0.30 / 1.15 = 0.26

# 重み付き統合
final_score = 0.35×pred1 + 0.39×pred2 + 0.26×pred3
```

### 3. Stacking（スタッキング）

**メタモデルで最適統合を学習**：

```python
# Level 1: 各作戦の予測
predictions = [
    basic_win_prob_pred,
    learning_to_rank_pred,
    odds_value_hunter_pred,
    combo_affinity_pred,
    condition_specialist_pred,
]

# Level 2: メタモデル（LightGBM）
meta_features = predictions  # 特徴量として使用
meta_model.predict(meta_features)  # 最終予測
```

## 実装

### スクリプト

1. **`analysis/ensemble_hybrid/collect_predictions.py`**
   - 各作戦の予測を収集・統一フォーマット化

2. **`analysis/ensemble_hybrid/voting_ensemble.py`**
   - Hard/Soft Voting実装

3. **`analysis/ensemble_hybrid/weighted_ensemble.py`**
   - 重み付きアンサンブル

4. **`analysis/ensemble_hybrid/stacking_meta_learner.py`**
   - スタッキングメタ学習

5. **`analysis/ensemble_hybrid/optimize_weights.py`**
   - グリッドサーチで最適重み探索

### データ形式

**strategy_predictions テーブル（要作成）**
```sql
CREATE TABLE strategy_predictions (
  id INTEGER PRIMARY KEY,
  race_id INTEGER,
  horse_id INTEGER,
  strategy_id VARCHAR,
  prediction_score REAL,
  predicted_rank INTEGER,
  created_at TIMESTAMP
);
```

## 評価指標

### 精度向上率
```
目標: 最良単一作戦より +20%以上
```

### 安定性（分散の低さ）
```
目標: 単一作戦より分散が小さい
```

### 相関分析
```
作戦間の相関: できるだけ低い方が良い
目標: 相関係数 < 0.7
```

## リスク・課題

### 1. 前提条件（重要度: 高）
- 各作戦の実装が必要
- **対策**: 優先度高の作戦から順次実装

### 2. 作戦間の相関（重要度: 中）
- 似た予測をする作戦ばかりだと効果減
- **対策**: 相関分析、独立性の高い作戦を選択

### 3. 計算コスト（重要度: 低）
- 全作戦を実行するため時間がかかる
- **対策**: 並列処理、キャッシュ

### 4. 過学習（重要度: 中）
- スタッキングで過学習のリスク
- **対策**: 時系列交差検証、正則化

## 改善案

1. **動的な重み調整**
   - 最近の性能で重みを変更
   - 調子が良い作戦を重視

2. **信頼度ベースの統合**
   - 確信度が高い作戦の予測を重視
   - 不確実性が高い予測は除外

3. **状況別の作戦選択**
   - 条件が揃った時は特化作戦を重視
   - 例: 稍重レース → condition-specialist重視

4. **ニューラルネットワーク**
   - メタ学習にディープラーニング適用

## 作戦の独立性分析

理想的な組み合わせ（相関が低い）:

| 作戦A | 作戦B | 相関 | 組み合わせ効果 |
|------|------|-----|-------------|
| basic-win-prob | learning-to-rank | 高 | △ |
| basic-win-prob | odds-value-hunter | 低 | ◎ |
| learning-to-rank | condition-specialist | 中 | ○ |
| combo-affinity | pace-scenario | 低 | ◎ |

## 次のステップ

- [ ] 各作戦の実装完了を待つ
- [ ] 予測結果を統一フォーマットで保存
- [ ] Hard/Soft Voting実装
- [ ] 重み付きアンサンブル実装
- [ ] スタッキング実装
- [ ] 最適重み探索（グリッドサーチ）
- [ ] 作戦間の相関分析

---

**作成日**: 2025-11-16
**最終更新**: 2025-11-16
