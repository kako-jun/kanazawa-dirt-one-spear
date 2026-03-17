# 作戦: 相性重視 (Combo Affinity)

**ID**: `combo-affinity`
**バージョン**: 1.0.0
**ステータス**: 計画中
**優先度**: 中

## 概要

**馬×騎手の相性**に注目した作戦。

過去の組み合わせ実績から「黄金コンビ」を発見し、相性の良いコンビが揃ったレースで勝負する。地方競馬は騎手が固定的なため、コンビデータが蓄積されやすい。

## 仮説

- **相性は存在する**: 馬と騎手には信頼関係、騎乗スタイルの一致がある
- **データに現れる**: 過去の成績から相性を定量化できる
- **地方競馬に有効**: 中央競馬より騎手が固定的で、コンビが形成されやすい
- **安定性が高い**: 相性が良いコンビは安定した成績を残す

## 王道（basic-win-prob）との違い

| 観点 | basic-win-prob | combo-affinity |
|------|----------------|----------------|
| 重視する要素 | 個別の実力 | 組み合わせの相性 |
| 特徴量 | 累積統計のみ | コンビスコア追加 |
| 期待する効果 | 汎用性 | 安定性・一貫性 |
| 適したレース | すべて | コンビ経験がある |

## アルゴリズム

### 1. コンビスコアの計算

```python
def calculate_combo_score(horse_id, jockey_id):
    # stat_horse_jockey_comboから取得
    combo = get_combo_stats(horse_id, jockey_id)

    if combo is None or combo['races'] < 3:
        # 経験不足の場合は調教師×騎手で代用
        return calculate_trainer_jockey_score(horse_id, jockey_id)

    score = (
        0.5 * combo['win_rate'] +
        0.3 * combo['place_rate'] +
        0.2 * (1 / combo['avg_finish_position'])
    )

    # 厩舎所属騎手ボーナス
    if is_stable_jockey(horse_id, jockey_id):
        score *= 1.1

    return score
```

### 2. 特徴量エンジニアリング

```python
features = {
    # 基本特徴量（basic-win-probと同じ）
    'horse_cumulative_stats': ...,
    'jockey_cumulative_stats': ...,
    'trainer_cumulative_stats': ...,
    'race_conditions': ...,

    # コンビ特徴量（新規）
    'combo_score': calculate_combo_score(horse_id, jockey_id),
    'combo_experience': combo['races'],  # 経験回数
    'combo_recent_form': get_recent_combo_form(horse_id, jockey_id, days=90),
    'is_stable_jockey': is_stable_jockey(horse_id, jockey_id),
    'trainer_jockey_combo_score': calculate_trainer_jockey_score(trainer_id, jockey_id),
}
```

### 3. 予測方法

```
1. 各馬×騎手のコンビスコアを計算
   horse_1 × jockey_A: 0.35（黄金コンビ！）
   horse_2 × jockey_B: 0.20（普通）
   horse_3 × jockey_C: 0.15（経験少ない）

2. コンビスコアを含めて勝率予測
   model.predict(features + combo_score)

3. 相性が良いコンビが多いレースは狙い目
   例: コンビスコア0.3以上が3頭以上 → 確信度高

4. 上位3頭で3連単を構築
```

## 実装

### スクリプト

1. **`analysis/combo_affinity/calculate_combo_score.py`**
   - コンビスコア計算ロジック
   - 統計的有意性検定

2. **`analysis/combo_affinity/feature_engineering.py`**
   - コンビ関連特徴量生成
   - 調教師×騎手の相性も考慮

3. **`analysis/combo_affinity/train_combo_model.py`**
   - LightGBM訓練（コンビ特徴量込み）

4. **`analysis/combo_affinity/predict_combo_trifecta.py`**
   - 本番用の3連単予想

### 使用テーブル

- **stat_horse_jockey_combo**（最重要！）
  - 馬×騎手ごとの成績
  - 勝率、複勝率、平均着順、レース数
- stat_horse_cumulative
- stat_jockey_cumulative
- stat_trainer_cumulative
- stat_recent_form_jockey

## 評価指標

### 的中率（安定性重視）
```
目標: 5%以上（basic-win-probと同等以上）
```

### 分散の低さ
```
標準偏差: basic-win-probより小さい
→ 安定性が高い
```

### コンビスコアの予測力
```
Feature Importance: combo_scoreが上位に入るか
```

## リスク・課題

### 1. コンビ経験が少ない（重要度: 中）
- 初めての組み合わせや経験回数が少ない場合、データ不足
- **対策**: 調教師×騎手で補完、最低経験回数を設定

### 2. 相性が偶然の可能性（重要度: 中）
- サンプルサイズが小さいと偶然の成績を相性と誤認
- **対策**: 統計的有意性検定（t検定など）、最低5回以上の経験を要求

### 3. basic-win-probとの差異が小さい（重要度: 低）
- コンビ特徴量が既存の特徴量と相関している可能性
- **対策**: 実験で効果を検証、差がなければ統合

## 改善案

1. **馬×調教師の相性**
   - 調教スタイルとの相性も重要

2. **厩舎内の人間関係データ**
   - 所属騎手、主戦騎手の情報を活用

3. **騎乗依頼のパターン学習**
   - 珍しい組み合わせ = 本気の勝負？
   - 普段と違う騎手 = 何か意図がある？

## データ分析計画

### 確認項目

1. **コンビデータの充実度**
   ```sql
   SELECT
     MIN(races) as min_races,
     AVG(races) as avg_races,
     MAX(races) as max_races
   FROM stat_horse_jockey_combo;
   ```

2. **相性の統計的有意性**
   - 相性が良いコンビは本当に有意に成績が良いか？
   - ランダムなコンビとの比較

3. **Feature Importance**
   - combo_scoreは本当に予測に寄与するか？

### 実験設計

```python
# コンビあり vs なしの比較
model_with_combo = LightGBM(features + combo_features)
model_without_combo = LightGBM(features)

# 性能比較
print("With Combo:", model_with_combo.score())
print("Without Combo:", model_without_combo.score())

# Feature Importance
print(model_with_combo.feature_importances_)
```

## 次のステップ

- [ ] stat_horse_jockey_comboテーブルの分析
- [ ] コンビスコア計算ロジック実装
- [ ] 統計的有意性検定
- [ ] 特徴量エンジニアリング
- [ ] basic-win-probとの比較実験

---

**作成日**: 2025-11-16
**最終更新**: 2025-11-16
