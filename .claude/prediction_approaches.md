# 予想アルゴリズムのアプローチ

## 概要

予想システムは**2つの独立したルート**で開発し、最終的に比較・統合する。

### ルートA: 解釈可能な機械学習（ホワイトボックス）
- 各特徴量の重みを調整
- **なぜその予想になったか説明できる**
- LightGBM、ロジスティック回帰など

### ルートB: ディープラーニング（ブラックボックス）
- 大量データを与えて学習
- **説明不可能だが高精度の可能性**
- ニューラルネットワーク、Transformer

両方を試し、結果を比較してベストな手法を採用する。

---

## ルートA: 解釈可能な機械学習

### 基本的な流れ

```
[1] 特徴量エンジニアリング
  各観点（枠番、オッズ、前走成績など）を数値化
  ↓
[2] モデル学習
  LightGBMなどで各特徴量の重みを自動学習
  ↓
[3] 重み調整（ハイパーパラメータチューニング）
  精度が最大になるように重みを探索
  ↓
[4] 予想生成
  各馬にスコアを付け、上位3頭を3連単として出力
  ↓
[5] 説明可能性の確保
  SHAP値で「なぜこの馬を選んだか」を説明
```

### 特徴量の例（観点）

各観点を数値化してモデルに入力:

```python
# 特徴量の例
features = {
    # 基本情報
    "gate_number": 3,              # 枠番
    "horse_number": 5,             # 馬番
    "odds": 4.2,                   # オッズ
    "popularity": 2,               # 人気順

    # 馬の情報
    "horse_age": 4,                # 馬齢
    "horse_weight": 485,           # 馬体重
    "weight_change": -3,           # 前走からの体重変化

    # 過去成績
    "last_1_rank": 2,              # 前走着順
    "last_3_avg_rank": 3.3,        # 過去3走平均着順
    "win_rate": 0.18,              # 通算勝率
    "place_rate": 0.45,            # 通算連対率

    # 騎手情報
    "jockey_win_rate": 0.22,       # 騎手勝率
    "jockey_experience": 1234,     # 騎手の騎乗回数

    # レース条件
    "distance": 1500,              # 距離
    "track_condition": 1,          # 馬場状態（良=1, 稍重=2...）
    "weather": 1,                  # 天候（晴=1, 曇=2...）

    # 相性
    "distance_win_rate": 0.21,     # この距離での勝率
    "track_condition_win_rate": 0.19,  # この馬場での勝率

    # 休養
    "days_since_last_race": 21,    # 前走からの日数
    "is_rest_comeback": 0,         # 休養明けフラグ

    # 調子
    "recent_trend": 0.15,          # 過去5走の成績トレンド（上昇=正）
}
```

### モデルの学習

**LightGBM Ranker**を使用:

```python
import lightgbm as lgb

# データ準備
train_data = lgb.Dataset(
    X_train,  # 特徴量行列
    label=y_train,  # ラベル（1着=1, 2着=2, ...）
    group=groups_train  # レースごとのグルーピング
)

# ハイパーパラメータ
params = {
    'objective': 'lambdarank',  # ランキング学習
    'metric': 'ndcg',  # 評価指標
    'num_leaves': 31,
    'learning_rate': 0.05,
    'feature_fraction': 0.9,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
}

# 学習
model = lgb.train(params, train_data, num_boost_round=100)

# 特徴量重要度を取得
importance = model.feature_importance(importance_type='gain')
```

### 重み調整（ハイパーパラメータチューニング）

**Optuna**を使って自動探索:

```python
import optuna

def objective(trial):
    # ハイパーパラメータをOptunaが提案
    params = {
        'num_leaves': trial.suggest_int('num_leaves', 10, 50),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
        'feature_fraction': trial.suggest_float('feature_fraction', 0.5, 1.0),
        # ...その他のパラメータ
    }

    # モデル学習
    model = lgb.train(params, train_data, num_boost_round=100)

    # 評価（的中率や回収率など）
    predictions = model.predict(X_val)
    accuracy = calculate_accuracy(predictions, y_val)

    return accuracy  # 最大化したい指標

# 100通りの組み合わせを試す
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)

# 最適なパラメータ
best_params = study.best_params
```

### 予想の生成

```python
# 各馬のスコアを予測
scores = model.predict(X_race)

# スコア上位3頭を取得
top_3_indices = np.argsort(scores)[:3]
first = entries[top_3_indices[0]]
second = entries[top_3_indices[1]]
third = entries[top_3_indices[2]]

# 3連単として出力
prediction = {
    "first": first.horse_number,
    "second": second.horse_number,
    "third": third.horse_number,
    "confidence": calculate_confidence(scores)
}
```

### 説明可能性（SHAP）

**なぜこの馬を選んだか**を説明:

```python
import shap

# SHAP値を計算
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_race[0])  # 1着予想馬

# 可視化
shap.waterfall_plot(shap.Explanation(
    values=shap_values,
    base_values=explainer.expected_value,
    data=X_race[0],
    feature_names=feature_names
))
```

**出力例**:
```
この馬を1着予想した理由:
+0.35: オッズが低い（2.8倍）
+0.22: 前走1着
+0.15: 内枠（3枠）
+0.08: 騎手勝率が高い
-0.05: やや休養明け（30日ぶり）
---
合計スコア: 0.75
```

### 終盤の作業（重み調整）

1. **特徴量の追加・削除**
   - 効果のない特徴量を削除
   - 新しい特徴量を試す

2. **ハイパーパラメータチューニング**
   - Optunaで100〜1000通り試す
   - 交差検証で過学習を防ぐ

3. **評価指標の調整**
   - 的中率重視 or 回収率重視
   - 指標に応じて最適化

4. **アンサンブル**
   - 複数モデルの予想を組み合わせ
   - LightGBM + XGBoost + CatBoost

---

## ルートB: ディープラーニング（ブラックボックス）

### 基本的な流れ

```
[1] データの埋め込み（Embedding）
  馬名、騎手名、厩舎名などを埋め込みベクトル化
  ↓
[2] ニューラルネットワークで学習
  大量のデータから自動的にパターン抽出
  ↓
[3] 予想生成
  各馬の勝率を予測し、上位3頭を出力
  ↓
[4] 精度評価
  ルートAと比較してどちらが良いか判定
```

### アーキテクチャ例

#### アプローチ1: TabNet（テーブルデータ向けDL）

```python
from pytorch_tabnet.tab_model import TabNetRegressor

model = TabNetRegressor(
    n_d=64,  # 決定次元
    n_a=64,  # 注意機構の次元
    n_steps=5,  # 推論ステップ数
    gamma=1.5,  # 特徴選択の強度
)

# 学習
model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    max_epochs=100,
)

# 予想
predictions = model.predict(X_race)
```

#### アプローチ2: Transformer（系列データ向け）

過去のレース履歴を系列データとして扱う:

```python
import torch
import torch.nn as nn

class RaceTransformer(nn.Module):
    def __init__(self, num_features, d_model=128, nhead=8):
        super().__init__()
        self.embedding = nn.Linear(num_features, d_model)
        self.transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model, nhead),
            num_layers=6
        )
        self.fc = nn.Linear(d_model, 1)  # 勝率予測

    def forward(self, x):
        # x: [batch, seq_len, num_features]
        # 過去10走のデータを系列として入力
        x = self.embedding(x)
        x = self.transformer(x)
        x = x.mean(dim=1)  # 平均プーリング
        return self.fc(x)

# モデル訓練
model = RaceTransformer(num_features=30)
optimizer = torch.optim.Adam(model.parameters())
criterion = nn.MSELoss()

for epoch in range(100):
    for batch in train_loader:
        optimizer.zero_grad()
        output = model(batch['features'])
        loss = criterion(output, batch['label'])
        loss.backward()
        optimizer.step()
```

#### アプローチ3: 埋め込み（Embedding）の活用

馬名・騎手名をベクトル化:

```python
class EmbeddingModel(nn.Module):
    def __init__(self, num_horses, num_jockeys, embedding_dim=32):
        super().__init__()
        self.horse_embedding = nn.Embedding(num_horses, embedding_dim)
        self.jockey_embedding = nn.Embedding(num_jockeys, embedding_dim)
        self.fc = nn.Linear(embedding_dim * 2 + other_features, 1)

    def forward(self, horse_id, jockey_id, other_features):
        horse_vec = self.horse_embedding(horse_id)
        jockey_vec = self.jockey_embedding(jockey_id)
        combined = torch.cat([horse_vec, jockey_vec, other_features], dim=1)
        return self.fc(combined)
```

### ブラックボックスの説明可能性

完全には説明できないが、部分的に可視化:

1. **Attention Weights**（Transformerの場合）
   - どの過去レースに注目したか

2. **Grad-CAM**
   - どの特徴量が重要だったか

3. **埋め込みベクトルの可視化**
   - 似た馬がクラスタになっているか

---

## 2つのルートの比較

### ルートA（ホワイトボックス）の利点

✅ **説明可能**: 「なぜこの予想か」がわかる
✅ **信頼性**: ユーザーに理屈を説明できる
✅ **デバッグしやすい**: 間違いの原因を特定可能
✅ **少ないデータでも動作**: 数千レースで十分

### ルートA の欠点

❌ **特徴量設計が必要**: 手動で特徴量を作る
❌ **複雑なパターン検出が苦手**: 非線形な関係の発見に限界

---

### ルートB（ブラックボックス）の利点

✅ **自動的にパターン発見**: 人間が気づかない関係も学習
✅ **大量データで強い**: データが増えるほど精度向上
✅ **特徴量エンジニアリング不要**: 生データを投げるだけ

### ルートB の欠点

❌ **説明不可能**: なぜその予想かわからない
❌ **過学習しやすい**: データが少ないと失敗
❌ **計算コスト高い**: GPUが必要な場合も
❌ **ユーザーの信頼を得にくい**: 「ブラックボックス」への不安

---

## 実装の優先順位

### フェーズ1: ルートAの基礎（現在〜3ヶ月）

1. 特徴量エンジニアリング
2. LightGBM実装
3. SHAP で説明可能性確保
4. 基本的なハイパーパラメータチューニング

**目標**: 的中率30%を目指す

---

### フェーズ2: ルートAの最適化（3〜6ヶ月）

5. 特徴量の追加（100個以上試す）
6. Optunaで徹底的にチューニング
7. アンサンブル学習（複数モデルの組み合わせ）
8. 回収率の最適化

**目標**: 的中率40%、回収率80%以上

---

### フェーズ3: ルートBの実験（6〜9ヶ月）

9. TabNet実装
10. Transformer実装
11. 埋め込みモデル実装
12. ルートAとの比較

**目標**: ルートAを超える精度を達成

---

### フェーズ4: 統合（9〜12ヶ月）

13. ルートAとBのアンサンブル
14. ユーザーに「ホワイトボックス予想」と「ブラックボックス予想」を両方提示
15. どちらが当たるか競争させる

**最終形態**: 2つの予想を並べて表示

```
┌────────────────────────────────────┐
│ 解釈可能AI予想（ルートA）          │
│ 1着: 3番  理由: オッズ低い、内枠  │
│ 2着: 7番  理由: 前走1着           │
│ 3着: 5番  理由: 騎手勝率高い      │
│ 信頼度: 72%                       │
└────────────────────────────────────┘

┌────────────────────────────────────┐
│ ディープラーニング予想（ルートB）  │
│ 1着: 5番  理由: 不明（AI判断）    │
│ 2着: 3番                          │
│ 3着: 8番                          │
│ 信頼度: 85%                       │
└────────────────────────────────────┘

どちらの予想を信じる？ → ユーザーが選択
```

---

## 終盤の作業（まとめ）

### ルートAの終盤作業

1. **特徴量の厳選**: 100個試して10個に絞る
2. **ハイパーパラメータチューニング**: Optunaで1000通り
3. **交差検証**: 年度別、月別で検証
4. **アンサンブル**: 複数モデルの投票
5. **閾値調整**: 信頼度が低い時は予想を出さない

**期間**: 1〜2ヶ月

### ルートBの終盤作業

1. **アーキテクチャ選択**: TabNet vs Transformer vs 両方
2. **データ拡張**: 過去データの水増し
3. **Early Stopping**: 過学習を防ぐ
4. **ハイパーパラメータチューニング**: 層数、ノード数など

**期間**: 1〜2ヶ月

---

## コンテンツ化

### ルートAの説明記事

- 「AIはこうやって予想している」
- 「SHAP値で見る予想の根拠」
- 「特徴量ランキング: 最も効く要素は？」

### ルートBの説明記事

- 「ディープラーニングの実験」
- 「説明不可能だが高精度なAI」
- 「ブラックボックスvs説明可能AI、どちらが勝つ？」

### 対決企画

- 毎週「ルートA vs ルートB」の的中率を公開
- ユーザー投票: 「今週はどちらを信じる？」
- 長期的な勝敗記録

---

## まとめ

### 2つのルートを並行開発

- **ルートA（ホワイトボックス）**: 説明可能、信頼性高い
- **ルートB（ブラックボックス）**: 高精度の可能性、実験的

### 最終的な統合: 「一本槍」+「参考予想」の2段構成

**コンセプトの維持**:
- サイト名「金沢ダート一本槍」は変えない
- **メイン予想（一本槍）= ホワイトボックスAI（ルートA）**
- 開発者自身が購入するのはこちら
- 大きく目立つ表示

**対決要素の追加**:
- **参考予想 = ディープラーニングAI（ルートB）**
- 小さめに表示、「実験的なAI予想」として紹介
- 毎週の的中率対決を記録

#### UI表示イメージ

```
┌─────────────────────────────────────────┐
│  🎯 金沢ダート一本槍                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━      │
│                                          │
│         穂先 → 3番                       │
│         団子 → 7番                       │
│         団子 → 5番                       │
│         柄                               │
│                                          │
│  信頼度: ★★★★☆ 72%                    │
│  💰 開発者も購入                         │
│                                          │
│  ━━ 予想の根拠 ━━━━━━━━━━━━━━        │
│  ✓ 3番: オッズ2.8倍、内枠、前走1着      │
│  ✓ 7番: 騎手勝率22%、この距離得意       │
│  ✓ 5番: 連対率45%、馬場適性あり         │
│                                          │
│  [この予想の詳細を見る]                  │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  🤖 参考: ディープラーニングAI予想       │
│  （実験的・説明不可能）  [折りたたむ]    │
├─────────────────────────────────────────┤
│  1着: 5番                                │
│  2着: 3番                                │
│  3着: 8番                                │
│  信頼度: 85%                             │
│                                          │
│  ⚠️ ブラックボックスAIのため、          │
│     なぜこの予想かは説明できません      │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  📊 今シーズンの対決成績                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━      │
│  🎯 一本槍（ホワイトボックス）           │
│     34勝 / 85戦  勝率: 40.0%            │
│                                          │
│  🤖 ディープラーニング                   │
│     38勝 / 85戦  勝率: 44.7%            │
│                                          │
│  今週はDLが僅差でリード！                │
│  [詳細な対決記録を見る]                  │
└─────────────────────────────────────────┘
```

#### UI/UXの工夫

**メイン予想（一本槍）**:
- 画面の上半分を占有
- 槍のビジュアルで目立たせる
- 「💰 開発者も購入」バッジで信頼感
- 予想の根拠を詳細に表示
- SHAP値グラフへのリンク

**参考予想（DL）**:
- 画面の下半分、小さめ
- 「実験的」「参考情報」と明記
- デフォルトで折りたたみ（興味ない人は非表示）
- 開くと予想が見える

**対決成績**:
- トップページにサマリー表示
- 別ページで詳細な比較
  - 週別の的中率グラフ
  - 累計の勝敗記録
  - 距離別・馬場別の得意不得意
  - 「今週はどちらが当たる？」ユーザー投票

#### コンテンツ展開

**ブログ記事**:
- 「一本槍 vs ディープラーニング、第1週目の結果」
- 「なぜホワイトボックスを一本槍に選んだか」
- 「ブラックボックスAIが驚異の勝率を記録」

**動画コンテンツ**（将来）:
- 対決のハイライト
- 予想が外れた週の分析
- 「今週はどちらを信じる？」討論

### すべての試行をコンテンツに

- 重み調整の過程を公開
- どのパラメータで精度が変わったか記録
- 失敗した実験も「検証結果」として価値化
- 2つのAIの特徴を比較記事化

**完全に無駄のない開発プロセス。**
**一本槍のコンセプトを保ちつつ、対決で楽しさ倍増。**
