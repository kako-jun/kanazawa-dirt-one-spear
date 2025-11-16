# 作戦: 順位予想型 (Learning to Rank)

**ID**: `learning-to-rank`
**バージョン**: 1.0.0
**ステータス**: 計画中
**優先度**: 高

## 概要

LightGBM Rankerを使って**レース内での順位を直接予測**する作戦。

従来の「勝率予測」ではなく、「馬同士の相対的な順位」を学習することで、3連単予想に最適化されたアプローチを実現する。

## 仮説

- **3連単は順位の問題である**: 勝率予測より順位予測が理論的に正しい
- **相対比較が重要**: 絶対的な強さではなく、レース内での相対関係が結果を決める
- **ランキング学習は最適**: LambdaMART/LambdaRankは順位予測のベストプラクティス

## なぜ王道（basic-win-prob）より優れているか？

| 観点 | basic-win-prob（勝率予測） | learning-to-rank（順位予測） |
|------|--------------------------|----------------------------|
| 予測対象 | 1着/非1着の二値分類 | レース内での順位（1〜8位） |
| 学習方法 | 独立した馬ごとの分類 | レース内の馬同士の相対比較 |
| クラス不均衡 | 深刻（1/8） | 緩和される（順位は分散） |
| 3連単への適合 | 間接的（上位3頭を選ぶ） | 直接的（順位そのもの） |
| 理論的正しさ | △（近似的） | ◎（最適化されている） |

## アルゴリズム

### モデル

#### 1. オッズなしモデル
**用途**: レース前の事前予想

**特徴量**:
- 馬の累積成績（勝率、複勝率、平均着順、休養日数）
- 騎手の累積成績（勝率、複勝率）
- 調教師の累積成績（勝率、複勝率）
- レース条件（馬場状態、距離カテゴリ）
- 枠番、馬番

**目的関数**: LambdaRank（順位を直接最適化）

#### 2. オッズありモデル
**用途**: オッズ発表後の最終予想

**特徴量**:
- 上記すべて + 人気順位

### 予想方法

```
1. レース内の全馬をグループとして順位スコアを予測
   race_id: 12345
     horse_1: score=8.5
     horse_2: score=7.2
     horse_3: score=6.8
     horse_4: score=5.1
     ...

2. スコアでソート
   1位: horse_1 (8.5)
   2位: horse_2 (7.2)
   3位: horse_3 (6.8)

3. 3連単を構築
   推奨: 1-2-3
```

## 実装

### スクリプト

1. **`analysis/learning_to_rank/feature_engineering.py`**
   - 特徴量生成（レース単位でgroup_id付与）
   - LightGBM Ranker用のデータ形式に変換

2. **`analysis/learning_to_rank/train_ranker.py`**
   - LightGBM Rankerの訓練
   - ハイパーパラメータチューニング

3. **`analysis/learning_to_rank/evaluate_ranker.py`**
   - 性能評価: NDCG@3, MAP@3, 的中率
   - basic-win-probとの比較

4. **`analysis/learning_to_rank/predict_trifecta.py`**
   - 本番用の3連単予想スクリプト

### 使用テーブル

- stat_horse_cumulative
- stat_jockey_cumulative
- stat_trainer_cumulative

### LightGBM Ranker の設定

```python
import lightgbm as lgb

# データ準備
train_data = lgb.Dataset(
    X_train,
    label=y_train,  # 順位（1, 2, 3, ..., 8）
    group=group_sizes,  # レースごとの馬の頭数（例: [8, 8, 7, 8, ...]）
)

# パラメータ
params = {
    'objective': 'lambdarank',
    'metric': 'ndcg',
    'ndcg_eval_at': [1, 3, 5],  # 上位1, 3, 5頭の精度
    'learning_rate': 0.05,
    'num_leaves': 31,
    'max_depth': -1,
}

# 訓練
model = lgb.train(params, train_data, num_boost_round=100)
```

## 評価指標

### NDCG@3 (Normalized Discounted Cumulative Gain)
- **意味**: 上位3頭の順位予測精度
- **目標**: 0.8以上

### MAP@3 (Mean Average Precision)
- **意味**: 上位3頭に正解が含まれる精度
- **目標**: 0.5以上

### 3連単的中率
- **意味**: 実際に1-2-3が当たる確率
- **目標**: 5%以上（ベースライン: 1/336 = 0.3%）

## リスク・課題

### 1. データ準備の複雑さ（重要度: 中）
- LightGBM Rankerは`group_id`を正しく設定する必要がある
- **対策**: race_idをgroup_idとして使用

### 2. 評価指標の理解（重要度: 低）
- NDCG, MAPなど専門的な指標
- **対策**: ドキュメント整備、可視化

### 3. 計算コスト（重要度: 低）
- グループごとの処理が必要
- **対策**: 最適化、GPU活用

## 改善案

1. **上位N頭の確率分布**
   - 順位1位の確率、2位の確率などを予測
   - 複数パターンの3連単を生成

2. **ペア単位の比較（Pairwise Ranking）**
   - 馬AとBのどちらが上か、を直接学習
   - より細かい順位関係を捉える

3. **アンサンブル**
   - Ranker + Classifier の組み合わせ
   - 相互補完

## basic-win-probとの比較実験

| 項目 | basic-win-prob | learning-to-rank |
|------|----------------|------------------|
| 手法 | 二値分類 | ランキング学習 |
| 訓練時間 | ベースライン | ? |
| NDCG@3 | ? | ? |
| 的中率 | ? | ? |
| 回収率 | ? | ? |

## 次のステップ

- [ ] 特徴量エンジニアリング実装
- [ ] LightGBM Ranker訓練スクリプト作成
- [ ] 時系列交差検証
- [ ] basic-win-probと比較
- [ ] ハイパーパラメータチューニング

---

**作成日**: 2025-11-16
**最終更新**: 2025-11-16
