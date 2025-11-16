# 作戦: 展開予想型 (Pace Scenario)

**ID**: `pace-scenario`
**バージョン**: 1.0.0
**ステータス**: 計画中
**優先度**: 低

## 概要

**レース展開（ペース）**を予測して有利な脚質の馬を選ぶ作戦。

競馬は相対的な競技であり、周囲の馬との兼ね合いで結果が変わる。逃げ馬が多いレースは差し馬有利、逃げ馬が少ないレースは逃げ馬有利など、展開を読んで馬券を選択する上級者向けアプローチ。

## 仮説

- **展開は結果を左右する**: ペースが向けば普段以上の力を発揮する
- **脚質は推定可能**: コーナー通過順から逃げ/先行/差し/追込を判定できる
- **ペースは予測可能**: 過去の脚質傾向から今回のペースを予測できる
- **地方競馬でも有効**: 中央競馬ほど分析されていないため、差別化要因になる

## 競馬における脚質とペース

### 脚質の分類

| 脚質 | 特徴 | コーナー通過順 |
|------|------|--------------|
| 逃げ | 先頭を走る | 1-2コーナーで1-2位 |
| 先行 | 前の方を走る | 1-2コーナーで3-5位 |
| 差し | 後方から追い上げ | 1-2コーナーで6位以下 → 3-4コーナーで上昇 |
| 追込 | 最後方から一気 | 1-2コーナーで最後方 → 直線で一気 |

### ペースと有利な脚質

| ペース | 状況 | 有利な脚質 |
|--------|------|-----------|
| ハイペース | 逃げ・先行馬が多い、前半が速い | 差し・追込 |
| 平均ペース | バランスが取れている | すべて |
| スローペース | 逃げ・先行馬が少ない、前半が遅い | 逃げ・先行 |

## 王道（basic-win-prob）との違い

| 観点 | basic-win-prob | pace-scenario |
|------|----------------|---------------|
| 重視する要素 | 個別の実力 | レース展開 |
| 予測対象 | 馬の勝率 | ペース + 脚質適性 |
| 難易度 | 低 | 高（上級者向け） |
| データ要件 | 基本統計のみ | コーナー通過順が必須 |
| 効果 | 汎用的 | 展開が読めた時に高精度 |

## アルゴリズム

### 1. 脚質の推定

コーナー通過順から各馬の脚質を推定する。

```python
def estimate_running_style(corner_positions, finish_position):
    """
    コーナー通過順から脚質を推定
    """
    c1, c2, c3, c4 = corner_positions

    # 前半（1-2コーナー）の平均順位
    early_position = (c1 + c2) / 2

    # 後半（3-4コーナー）の平均順位
    late_position = (c3 + c4) / 2

    # 追い上げ度
    closing_power = early_position - late_position

    if early_position <= 2:
        return "逃げ"
    elif early_position <= 5:
        if closing_power < -1:
            return "先行"
        else:
            return "差し"
    else:
        if closing_power > 2:
            return "追込"
        else:
            return "差し"
```

### 2. ペースの予測

レース内の脚質構成からペースを予測する。

```python
def predict_pace(horses):
    """
    レースのペースを予測
    """
    running_styles = [h.running_style for h in horses]

    front_runners = sum(1 for s in running_styles if s in ["逃げ", "先行"])
    closers = sum(1 for s in running_styles if s in ["差し", "追込"])

    if front_runners >= 5:
        return "ハイペース"  # 前に馬が多い → ハイペース
    elif front_runners <= 2:
        return "スローペース"  # 前に馬が少ない → スローペース
    else:
        return "平均ペース"
```

### 3. 展開向き度の計算

```python
def calculate_pace_advantage(running_style, predicted_pace):
    """
    展開向き度を計算（-1〜+1）
    """
    advantage_matrix = {
        ("逃げ", "ハイペース"): -1,
        ("逃げ", "平均ペース"): 0,
        ("逃げ", "スローペース"): +1,
        ("先行", "ハイペース"): -0.5,
        ("先行", "平均ペース"): 0,
        ("先行", "スローペース"): +0.5,
        ("差し", "ハイペース"): +1,
        ("差し", "平均ペース"): 0,
        ("差し", "スローペース"): -1,
        ("追込", "ハイペース"): +1,
        ("追込", "平均ペース"): 0,
        ("追込", "スローペース"): -1,
    }

    return advantage_matrix.get((running_style, predicted_pace), 0)
```

### 4. 予測方法

```
1. 各馬の脚質を推定
   horse_1: 逃げ
   horse_2: 先行
   horse_3: 先行
   horse_4: 差し
   horse_5: 追込

2. レース全体のペースを予測
   逃げ・先行: 3頭 → 平均ペース

3. 展開向き度を計算
   horse_1（逃げ）: 平均ペース → 0
   horse_4（差し）: 平均ペース → 0
   horse_5（追込）: 平均ペース → 0

4. 展開特徴量を含めて勝率予測
   model.predict(features + [running_style, predicted_pace, pace_advantage])

5. 展開が向いた馬を重視して3連単構築
```

## 実装

### スクリプト

1. **`analysis/pace_scenario/estimate_running_style.py`**
   - 脚質推定（コーナー通過順から）
   - 過去レースの脚質を一括計算

2. **`analysis/pace_scenario/predict_pace.py`**
   - レースペース予測
   - 脚質構成から判定

3. **`analysis/pace_scenario/calculate_pace_advantage.py`**
   - 展開向き度の計算
   - 脚質×ペースのマトリクス

4. **`analysis/pace_scenario/train_pace_model.py`**
   - LightGBM訓練（展開特徴量込み）

5. **`analysis/pace_scenario/predict_pace_trifecta.py`**
   - 本番用の3連単予想

### 使用テーブル

- race_performances（最重要！）
  - corner_1_position
  - corner_2_position
  - corner_3_position
  - corner_4_position
- stat_horse_cumulative
- stat_jockey_cumulative
- stat_trainer_cumulative

### 新規テーブル（要作成）

```sql
CREATE TABLE running_style_history (
  id INTEGER PRIMARY KEY,
  horse_id INTEGER,
  race_id INTEGER,
  running_style VARCHAR,  -- 逃げ/先行/差し/追込
  early_position REAL,    -- 前半平均順位
  late_position REAL,     -- 後半平均順位
  closing_power REAL,     -- 追い上げ度
  created_at TIMESTAMP
);
```

## 評価指標

### 展開向き時の的中率
```
pace_advantage > 0.5 の時の的中率: 8%以上
目標: basic-win-probの1.5倍
```

### 脚質推定の精度
```
手動ラベルとの一致率: 80%以上
```

### ペース予測の精度
```
実際のラップタイムとの相関: 0.6以上
```

## リスク・課題

### 1. コーナー通過順データの欠損（重要度: 高）
- データが欠けていると脚質推定不可
- **対策**: まずデータ確認、欠損が多ければ作戦を見送り

### 2. 脚質推定が不正確（重要度: 中）
- 単純なルールベースでは精度に限界
- **対策**: 手動でサンプルを確認、ロジックを改善

### 3. ペース予測が難しい（重要度: 中）
- 実際のペースは騎手の判断で変わる
- **対策**: 単純化（逃げ馬の数のみで判定）

### 4. 実装が複雑（重要度: 低）
- 他の作戦より実装難易度が高い
- **対策**: 段階的に実装、まずは脚質推定から

## 改善案

1. **ラップタイム分析**
   - 前半・後半の速度を実測
   - より正確なペース判定

2. **騎手の脚質傾向**
   - この騎手は逃げが多い、など
   - 騎手×脚質のクロス集計

3. **馬の脚質適性学習**
   - 本来は差し馬だが今回は先行、など
   - 適性外の脚質は警戒

4. **展開パターンのクラスタリング**
   - 似た展開のレースをグループ化
   - パターン別の傾向分析

## データ確認計画

### 最優先: コーナー通過順の確認

```sql
SELECT
  COUNT(*) as total_performances,
  SUM(CASE WHEN corner_1_position IS NOT NULL THEN 1 ELSE 0 END) as has_corner_1,
  SUM(CASE WHEN corner_2_position IS NOT NULL THEN 1 ELSE 0 END) as has_corner_2,
  SUM(CASE WHEN corner_3_position IS NOT NULL THEN 1 ELSE 0 END) as has_corner_3,
  SUM(CASE WHEN corner_4_position IS NOT NULL THEN 1 ELSE 0 END) as has_corner_4
FROM race_performances;
```

**判断基準**:
- 80%以上データがある → 実装可能
- 50-80% → 部分的に実装
- 50%未満 → 作戦を見送り

## 次のステップ

- [ ] **最優先**: race_performancesのcorner_1〜4_positionデータを確認
- [ ] データが十分なら脚質推定ロジック実装
- [ ] running_style_historyテーブル作成
- [ ] ペース予測ロジック実装
- [ ] basic-win-probとの比較実験

---

**作成日**: 2025-11-16
**最終更新**: 2025-11-16
