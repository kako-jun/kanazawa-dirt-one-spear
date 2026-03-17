# 作戦: 条件スペシャリスト (Condition Specialist)

**ID**: `condition-specialist`
**バージョン**: 1.0.0
**ステータス**: 計画中
**優先度**: 中

## 概要

**馬場状態・距離の適性**に注目した作戦。

「この馬は重馬場が得意」「この馬は短距離専門」など、条件が合致した時に能力を最大限発揮する馬を見つけて勝負する。

## 仮説

- **適性は存在する**: 馬には得意な馬場状態や距離がある
- **条件が揃えば激変**: 普段は凡走でも、得意条件では上位に来る
- **データに現れる**: stat_horse_track_condition, stat_horse_distance_categoryに有効な情報
- **人気に織り込まれにくい**: 一般ファンは条件適性を過小評価しがち

## 競馬における条件適性の例

### 馬場状態適性

| 馬場状態 | 特徴 | 適した馬 |
|---------|------|---------|
| 良 | 固い、スピード勝負 | パワーより脚質重視 |
| 稍重 | やや柔らかい | バランス型 |
| 重 | 柔らかい、パワー勝負 | パワーがある馬 |
| 不良 | 泥濘、スタミナ勝負 | タフな馬、ダート適性 |

### 距離適性

| 距離カテゴリ | 金沢競馬 | 適した馬 |
|------------|---------|---------|
| 短距離 | 1400m以下 | スピード型、瞬発力 |
| マイル | 1500m | バランス型 |
| 中距離 | 1700m-2000m | スタミナ型 |
| 長距離 | 2100m以上 | 持久力重視 |

## 王道（basic-win-prob）との違い

| 観点 | basic-win-prob | condition-specialist |
|------|----------------|---------------------|
| 重視する要素 | 累積実力 | 条件適性 |
| 狙うレース | すべて | 得意条件が揃ったレース |
| 期待する効果 | 汎用性 | 条件マッチ時の高精度 |
| リスク | 平均的 | 条件が揃わないと弱い |

## アルゴリズム

### 1. 条件適性スコアの計算

```python
def calculate_condition_affinity(horse_id, track_condition, distance_category):
    # stat_horse_track_conditionから取得
    track_stats = get_track_condition_stats(horse_id, track_condition)
    distance_stats = get_distance_stats(horse_id, distance_category)

    if track_stats is None or track_stats['races'] < 3:
        track_win_rate = 0.0
    else:
        track_win_rate = track_stats['win_rate']

    if distance_stats is None or distance_stats['races'] < 3:
        distance_win_rate = 0.0
    else:
        distance_win_rate = distance_stats['win_rate']

    # 騎手・調教師の適性も考慮
    jockey_track = get_jockey_track_stats(jockey_id, track_condition)
    trainer_distance = get_trainer_distance_stats(trainer_id, distance_category)

    score = (
        0.4 * track_win_rate +
        0.4 * distance_win_rate +
        0.1 * jockey_track['win_rate'] +
        0.1 * trainer_distance['win_rate']
    )

    return score
```

### 2. 得意条件の判定

```python
# 得意条件フラグ
is_favorite_condition = (condition_affinity_score > 0.2)

# 条件が揃ったレースのみ狙う戦略
if sum(is_favorite_condition for horse in race) >= 3:
    # 3頭以上が得意条件 → 混戦、見送り
    pass
elif sum(is_favorite_condition for horse in race) == 1:
    # 1頭だけが得意条件 → 狙い目！
    target_horse = [h for h in race if h.is_favorite_condition][0]
```

### 3. 予測方法

```
1. 今回のレース条件を取得
   track_condition = "稍重"
   distance = 1400m → distance_category = "短距離"

2. 各馬の条件適性スコアを計算
   horse_1: track=0.30, distance=0.25 → score=0.28（得意！）
   horse_2: track=0.10, distance=0.35 → score=0.23（まあまあ）
   horse_3: track=0.05, distance=0.08 → score=0.07（苦手）

3. 条件スコアを特徴量に加えて勝率予測
   model.predict(features + condition_affinity_score)

4. 得意条件が揃った馬を重視して3連単構築
```

## 実装

### スクリプト

1. **`analysis/condition_specialist/calculate_condition_score.py`**
   - 条件適性スコア計算ロジック

2. **`analysis/condition_specialist/feature_engineering.py`**
   - 条件関連特徴量生成

3. **`analysis/condition_specialist/train_condition_model.py`**
   - LightGBM訓練（条件特徴量込み）

4. **`analysis/condition_specialist/predict_condition_trifecta.py`**
   - 本番用の3連単予想

### 使用テーブル

- **stat_horse_track_condition**（最重要！）
  - 馬×馬場状態ごとの成績
- **stat_horse_distance_category**（最重要！）
  - 馬×距離カテゴリごとの成績
- stat_jockey_track_condition
- stat_jockey_distance_category
- stat_trainer_track_condition
- stat_trainer_distance_category

## 評価指標

### 条件マッチ時の的中率
```
得意条件が揃った時の的中率: 10%以上
目標: basic-win-probの2倍
```

### 精度（Precision）
```
「得意条件」と判定した時の的中率
目標: 高精度
```

### 再現率（Recall）
```
実際に得意条件で勝った馬を事前に判定できたか
目標: 70%以上
```

## リスク・課題

### 1. 条件が揃うレースが少ない（重要度: 中）
- 得意条件が揃うレースが限られる
- **対策**: 条件の定義を緩和、複数条件を組み合わせ

### 2. データ不足（重要度: 中）
- 特定条件の経験が少ない馬がいる
- **対策**: 最低経験回数を設定、累積統計で補完

### 3. 過学習のリスク（重要度: 低）
- 条件を細かく分けすぎると過学習
- **対策**: 交差検証、正則化

## 改善案

1. **天候との組み合わせ**
   - 雨×重馬場など、天候も考慮

2. **季節・月別の適性**
   - 夏競馬が得意、冬競馬が得意など

3. **コース形状**
   - 直線長、コーナー数、高低差など

4. **複合条件の学習**
   - 稍重×1400m、重×1900m など
   - 条件の組み合わせパターンを学習

## データ分析計画

### 確認項目

1. **条件別データの充実度**
   ```sql
   SELECT
     track_condition,
     COUNT(*) as races,
     AVG(win_rate) as avg_win_rate
   FROM stat_horse_track_condition
   GROUP BY track_condition;
   ```

2. **適性の統計的有意性**
   - 得意条件で本当に成績が良いか？
   - ランダムな差との比較

3. **Feature Importance**
   - condition_affinity_scoreは本当に予測に寄与するか？

### 実験設計

```python
# 条件あり vs なしの比較
model_with_condition = LightGBM(features + condition_features)
model_without_condition = LightGBM(features)

# 性能比較
print("With Condition:", model_with_condition.score())
print("Without Condition:", model_without_condition.score())

# 得意条件マッチ時のみの精度
condition_matched_data = data[data['is_favorite_condition'] == True]
print("Condition Matched Hit Rate:", model.hit_rate(condition_matched_data))
```

## 次のステップ

- [ ] stat_horse_track_condition, stat_horse_distance_categoryテーブルの分析
- [ ] 条件適性スコア計算ロジック実装
- [ ] 得意条件の定義と閾値設定
- [ ] 特徴量エンジニアリング
- [ ] basic-win-probとの比較実験

---

**作成日**: 2025-11-16
**最終更新**: 2025-11-16
