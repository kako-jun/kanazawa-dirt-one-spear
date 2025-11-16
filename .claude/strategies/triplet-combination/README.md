# 作戦: トリプレット組み合わせ型 (Triplet Combination)

**ID**: `triplet-combination`
**バージョン**: 1.0.0
**ステータス**: 計画中
**優先度**: 高

## 概要

**3頭の組み合わせを直接スコアリング**する究極の3連単特化型アプローチ。

馬を個別に評価するのではなく、**3頭セット**として評価する。「この3頭が揃うと強い」「相性が良い組み合わせ」など、3頭の相互作用・シナジーを捉える。全336通りの組み合わせを評価し、**オッズとスコアの乖離が大きい組み合わせ（万馬券の鍵）** を発見する。

## 仮説

- **馬同士には相性がある**: 単独の実力の足し算ではない
- **3頭のシナジー**: 組み合わせによって展開が変わる
- **ペースバランス**: 逃げ・先行・差しのバランスが重要
- **336通りを全評価**: 見落としがちな組み合わせをAIが発見
- **万馬券の法則**: オッズが高いが実は確率も高い組み合わせが存在

## 従来手法との違い

| 手法 | 評価対象 | 3連単への適合 |
|------|---------|-------------|
| basic-win-prob | 各馬を個別評価 → 上位3頭 | 間接的 |
| learning-to-rank | 各馬の順位を予測 → 上位3頭 | やや直接的 |
| **triplet-combination** | **3頭セットを直接評価** | **完全に最適化** |

```
従来:
  馬A: score=0.25
  馬B: score=0.18
  馬C: score=0.15
  → 3連単: A-B-C

triplet-combination:
  (A, B, C): score=0.12
  (A, C, D): score=0.15  ← こちらが高い！
  (B, C, E): score=0.10
  → 3連単: A-C-D
```

## アルゴリズム

### 1. 全組み合わせ生成

```python
from itertools import permutations

def generate_all_trifectas(horses):
    """
    全ての3連単組み合わせを生成

    Args:
        horses: レース内の馬リスト

    Returns:
        全336通りの組み合わせ（8頭立ての場合）
    """
    from itertools import permutations

    # 順列を生成（順序が重要）
    triplets = list(permutations(horses, 3))

    print(f"組み合わせ数: {len(triplets)}通り")
    return triplets
```

### 2. シナジースコア計算

```python
def calculate_synergy_score(triplet):
    """
    3頭の組み合わせシナジースコアを計算

    Args:
        triplet: (horse1, horse2, horse3)

    Returns:
        synergy_score: 0-1のスコア
    """
    h1, h2, h3 = triplet

    # 1. 脚質バランス（ペース）
    running_styles = [h1.running_style, h2.running_style, h3.running_style]
    pace_balance_score = evaluate_pace_balance(running_styles)

    # 2. 騎手スキルの合計
    jockey_skill = (h1.jockey.win_rate + h2.jockey.win_rate + h3.jockey.win_rate) / 3

    # 3. 枠番の分散（バランス）
    gates = [h1.gate_number, h2.gate_number, h3.gate_number]
    gate_variance = np.var(gates)
    gate_balance_score = 1 / (1 + gate_variance)  # 分散が小さいほど高スコア

    # 4. 過去の共演回数（このメンバーで走ったことがあるか）
    cooccurrence = get_historical_cooccurrence(h1, h2, h3)

    # 統合スコア
    synergy_score = (
        0.4 * pace_balance_score +
        0.3 * jockey_skill +
        0.2 * gate_balance_score +
        0.1 * cooccurrence
    )

    return synergy_score


def evaluate_pace_balance(running_styles):
    """
    脚質バランスを評価

    理想的: 逃げ1頭、先行1頭、差し1頭
    """
    style_counts = Counter(running_styles)

    # 多様性が高いほど良い
    diversity = len(set(running_styles)) / 3

    # 逃げが多すぎるとハイペース → 差し有利
    if style_counts['逃げ'] >= 2:
        return 0.3  # 低スコア

    # バランスが取れている
    return diversity
```

### 3. Triplet Network（ディープラーニング）

```python
import torch
import torch.nn as nn

class TripletNetwork(nn.Module):
    """
    3頭の組み合わせを学習するニューラルネットワーク
    """
    def __init__(self, feature_dim=16):
        super().__init__()

        # 各馬の特徴量を埋め込み
        self.horse_embedding = nn.Sequential(
            nn.Linear(feature_dim, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 32),
            nn.ReLU(),
        )

        # 3頭の特徴量を統合
        self.combination_layer = nn.Sequential(
            nn.Linear(32 * 3, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid(),  # 0-1の確率
        )

    def forward(self, horse1_features, horse2_features, horse3_features):
        # 各馬を埋め込み
        h1 = self.horse_embedding(horse1_features)
        h2 = self.horse_embedding(horse2_features)
        h3 = self.horse_embedding(horse3_features)

        # 結合
        combined = torch.cat([h1, h2, h3], dim=1)

        # 3連単成立確率を予測
        prob = self.combination_layer(combined)

        return prob
```

### 4. 万馬券狙い（過小評価組み合わせ発見）

```python
def find_undervalued_triplets(triplets, scores, odds_data):
    """
    オッズの割に確率が高い組み合わせを発見

    Args:
        triplets: 全組み合わせ
        scores: 各組み合わせのスコア
        odds_data: オッズ情報

    Returns:
        過小評価されている組み合わせ（万馬券候補）
    """
    undervalued = []

    for triplet, score in zip(triplets, scores):
        # オッズから暗黙の確率を逆算
        estimated_odds = estimate_triplet_odds(triplet, odds_data)
        odds_implied_prob = 1 / estimated_odds if estimated_odds > 0 else 0

        # AIスコアとオッズ確率の乖離
        bias = score - odds_implied_prob

        # 期待値計算
        estimated_payout = estimated_odds * 100
        ev = score * estimated_payout - 100

        if ev > 50:  # 期待値が50円以上
            undervalued.append({
                'triplet': triplet,
                'score': score,
                'odds_prob': odds_implied_prob,
                'bias': bias,
                'ev': ev,
                'estimated_payout': estimated_payout,
            })

    # 期待値でソート
    undervalued.sort(key=lambda x: x['ev'], reverse=True)

    print("過小評価組み合わせ（万馬券候補）:")
    for item in undervalued[:10]:
        print(f"{item['triplet']}: EV={item['ev']:.0f}円 "
              f"スコア={item['score']:.2f} "
              f"配当={item['estimated_payout']:,}円")

    return undervalued
```

### 5. 組み合わせ最適化

```python
def select_best_triplets(triplets, scores, top_n=5):
    """
    スコア上位N個の組み合わせを選択

    複数買い戦略:
    - 1点買い: top_n=1
    - 5点買い: top_n=5（リスク分散）
    """
    scored_triplets = list(zip(triplets, scores))
    scored_triplets.sort(key=lambda x: x[1], reverse=True)

    top_triplets = scored_triplets[:top_n]

    print(f"トップ{top_n}の組み合わせ:")
    for i, (triplet, score) in enumerate(top_triplets, 1):
        print(f"{i}. {triplet}: score={score:.3f}")

    return [t[0] for t in top_triplets]
```

## 実装

### スクリプト

1. **`analysis/triplet_combination/generate_triplets.py`**
   - 全組み合わせ生成

2. **`analysis/triplet_combination/calculate_synergy.py`**
   - シナジースコア計算

3. **`analysis/triplet_combination/train_triplet_network.py`**
   - Triplet Network訓練（PyTorch）

4. **`analysis/triplet_combination/combinatorial_search.py`**
   - 組み合わせ最適化

5. **`analysis/triplet_combination/find_undervalued_triplets.py`**
   - 過小評価組み合わせ発見（万馬券狙い）

## 評価指標

### 3連単的中率
```
目標: 8%以上（全作戦中トップ）
```

### 万馬券的中率
```
配当10,000円以上の的中率: 3%以上
```

### 期待値
```
長期的な期待値: プラス（回収率100%超え）
```

## リスク・課題

### 1. 計算量（重要度: 高）
- 336通り × 8,733レース = 約300万組み合わせ
- **対策**: GPU並列化、事前フィルタリング

### 2. 訓練データ不足（重要度: 中）
- 同じ3頭の組み合わせは稀
- **対策**: 類似組み合わせでデータ拡張、転移学習

### 3. 過学習（重要度: 中）
- 複雑なモデルで過学習のリスク
- **対策**: 正則化、ドロップアウト、交差検証

## 次のステップ

- [ ] 全組み合わせ生成ロジック実装
- [ ] シナジースコア計算
- [ ] Triplet Network実装（PyTorch）
- [ ] 過小評価組み合わせ発見
- [ ] 万馬券バックテスト
- [ ] basic-win-probとの比較

---

**作成日**: 2025-11-16
**最終更新**: 2025-11-16
