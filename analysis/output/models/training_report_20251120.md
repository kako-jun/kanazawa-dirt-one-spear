# 作戦１「王道」モデル訓練レポート

**訓練日時**: 2025-11-20 16:33
**訓練環境**: GPU (NVIDIA GeForce GTX 1050 Ti, 4GB VRAM)
**使用ライブラリ**: LightGBM 4.6.0 + OpenCL
**データ期間**: 2015-2025年

---

## 訓練サマリー

### データ規模
- **総サンプル数**: 76,795
- **特徴量数**: 25（オッズなし）/ 26（オッズあり）
- **クラス分布**:
  - 1着（正例）: 8,692サンプル (11.32%)
  - 1着以外（負例）: 68,103サンプル (88.68%)

### クロスバリデーション
- **手法**: 時系列5-fold分割（リーク防止）
- **評価指標**: Accuracy, Precision, Recall, F1, ROC-AUC, LogLoss

---

## モデル1: オッズなしモデル (lightgbm_no_odds.pkl)

### 目的
レース前の事前予想（オッズ情報なしで純粋なAI判断）

### 特徴量（25個）
```
['gate_number', 'horse_number', 'distance', 'horse_count',
 'horse_total_races', 'horse_win_rate', 'horse_place_rate',
 'horse_avg_finish', 'horse_days_since_last_race',
 'jockey_total_races', 'jockey_win_rate', 'jockey_place_rate',
 'jockey_avg_finish', 'trainer_total_races', 'trainer_win_rate',
 'trainer_place_rate', 'track_不良', 'track_稍重', 'track_良', 'track_重',
 'distance_1300-1400m', 'distance_1500-1600m', 'distance_1700-1800m',
 'distance_1900-2000m', 'distance_2100m-']
```

### 性能（5-fold CV平均）

| 指標 | 平均 | 標準偏差 |
|------|------|----------|
| Accuracy | 0.8853 | ±0.0019 |
| Precision | 0.4772 | ±0.1302 |
| Recall | 0.0068 | ±0.0026 |
| F1 Score | 0.0134 | ±0.0051 |
| ROC-AUC | 0.7279 | ±0.0221 |
| LogLoss | 0.3213 | ±0.0054 |

### Fold別詳細

#### Fold 1
- Accuracy: 0.8843, Precision: 0.3421, Recall: 0.0088, F1: 0.0172
- ROC-AUC: 0.7039, LogLoss: 0.3287

#### Fold 2
- Accuracy: 0.8881, Precision: 0.3333, Recall: 0.0069, F1: 0.0136
- ROC-AUC: 0.7051, LogLoss: 0.3212

#### Fold 3
- Accuracy: 0.8829, Precision: 0.6842, Recall: 0.0094, F1: 0.0185
- ROC-AUC: 0.7397, LogLoss: 0.3239

#### Fold 4
- Accuracy: 0.8843, Precision: 0.5263, Recall: 0.0069, F1: 0.0136
- ROC-AUC: 0.7625, LogLoss: 0.3122

#### Fold 5
- Accuracy: 0.8866, Precision: 0.5000, Recall: 0.0020, F1: 0.0041
- ROC-AUC: 0.7283, LogLoss: 0.3203

### 問題点
- **Recall 0.68%は極端に低い** - 実際の1着馬をほとんど予測できていない
- 保守的すぎて実用性に欠ける
- クラス不均衡の影響が顕著

---

## モデル2: オッズありモデル (lightgbm_with_odds.pkl)

### 目的
オッズ発表後の最終予想（人気情報を活用）

### 特徴量（26個）
上記25個 + `popularity`（人気順位）

### 性能（5-fold CV平均）

| 指標 | 平均 | 標準偏差 |
|------|------|----------|
| Accuracy | 0.8909 | ±0.0015 |
| Precision | 0.5557 | ±0.0159 |
| Recall | 0.2377 | ±0.0446 |
| F1 Score | 0.3304 | ±0.0442 |
| ROC-AUC | 0.8403 | ±0.0116 |
| LogLoss | 0.2697 | ±0.0049 |

### Fold別詳細

#### Fold 1
- Accuracy: 0.8886, Precision: 0.5379, Recall: 0.2075, F1: 0.2995
- ROC-AUC: 0.8254, LogLoss: 0.2785

#### Fold 2
- Accuracy: 0.8929, Precision: 0.5583, Recall: 0.1729, F1: 0.2641
- ROC-AUC: 0.8295, LogLoss: 0.2717

#### Fold 3
- Accuracy: 0.8897, Precision: 0.5770, Recall: 0.2347, F1: 0.3337
- ROC-AUC: 0.8566, LogLoss: 0.2655

#### Fold 4
- Accuracy: 0.8921, Precision: 0.5679, Recall: 0.2833, F1: 0.3781
- ROC-AUC: 0.8484, LogLoss: 0.2666

#### Fold 5
- Accuracy: 0.8912, Precision: 0.5372, Recall: 0.2900, F1: 0.3767
- ROC-AUC: 0.8418, LogLoss: 0.2664

### 評価
- **ROC-AUC 84.03%は優秀** - 確率予測として高精度
- **Recall 23.77%は実用的** - 約4レースに1回、1着馬を捕捉
- オッズなしモデルと比較して全指標で大幅改善

---

## モデル比較

### オッズ情報の効果

| 指標 | オッズなし | オッズあり | 改善率 |
|------|-----------|-----------|--------|
| Accuracy | 88.53% | 89.09% | +0.56pt |
| Precision | 47.72% | 55.57% | +7.85pt |
| **Recall** | **0.68%** | **23.77%** | **+23.09pt (35倍)** |
| **F1 Score** | **1.34%** | **33.04%** | **+31.70pt (25倍)** |
| **ROC-AUC** | **72.79%** | **84.03%** | **+11.24pt** |
| LogLoss | 0.3213 | 0.2697 | -0.0516 (改善) |

### 結論
**オッズ情報は極めて重要** - 特にRecallとF1スコアで劇的な改善

---

## 技術的詳細

### ハイパーパラメータ
```python
params = {
    'objective': 'binary',
    'metric': 'binary_logloss',
    'boosting_type': 'gbdt',
    'num_leaves': 31,
    'learning_rate': 0.05,
    'feature_fraction': 0.8,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
    'verbose': -1,
    'seed': 42,
    'device': 'gpu'  # GPU使用
}
```

### Early Stopping
- `num_boost_round`: 1000
- `early_stopping_rounds`: 50
- 実際の訓練ラウンド数: 約100ラウンド前後で収束

### GPU環境
- GPU: NVIDIA GeForce GTX 1050 Ti (4GB VRAM)
- ドライバ: 580.105.08
- CUDA: 13.0
- OpenCL: 3.0 CUDA 13.0.97

---

## 特徴量重要度

詳細は以下のファイルを参照：
- `feature_importance_no_odds.csv` / `.png`
- `feature_importance_with_odds.csv` / `.png`

---

## 既知の問題と改善案

### 1. クラス不均衡
**問題**: 1着は11.32%のみ（正例が少ない）
**影響**: オッズなしモデルのRecallが極端に低い
**改善案**:
- `scale_pos_weight`パラメータでクラス重み付け
- SMOTE（Synthetic Minority Over-sampling）
- 閾値調整（0.5以外の予測閾値）

### 2. 3連単予想の実装
**問題**: 現在は1着確率のみ予測
**次のステップ**:
- 上位N頭の組み合わせ生成
- 期待値ベースの選択（配当×確率）
- ランク学習への移行検討

### 3. バックテスト未実施
**必要性**: 実際の的中率・回収率を検証
**次のステップ**:
- 過去レースでの実購入シミュレーション
- 収益性の評価
- 購入戦略の最適化

---

## 次のアクション

- [ ] 特徴量重要度の詳細分析
- [ ] クラス重み付けによる再訓練
- [ ] バックテスト実装
- [ ] 3連単構築ロジックの実装
- [ ] API実装（予想エンドポイント）
- [ ] フロントエンドでの結果表示

---

## ファイル一覧

### 訓練済みモデル
- `lightgbm_no_odds.pkl` (258KB) - オッズなしモデル
- `lightgbm_with_odds.pkl` (284KB) - オッズありモデル

### 評価レポート
- `model_comparison.csv` - モデル性能比較表
- `training_report_20251120.md` - 本レポート

### 特徴量重要度
- `feature_importance_no_odds.csv` / `.png`
- `feature_importance_with_odds.csv` / `.png`

---

**作成日**: 2025-11-20
**作成者**: Claude Code + d131
**作戦ID**: basic-win-prob (作戦１「王道」)
