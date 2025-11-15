# Phase 2: 予想作戦構築フェーズ 戦略文書

**期間**: Phase 1完了後 〜 本番運用前
**目的**: 複数の予想アプローチを実装・比較し、最適な3連単予想手法を確立する

---

## Phase 2の核心的な問い

### 何が最も精度の良い3連単を出せるか、不明である

これが出発点。だから：
- **1つのアプローチに賭けない**
- **複数の仮説を試す**
- **実験的に比較する**
- **データから学ぶ**

---

## Phase 2で達成すること

### 1. 統計テーブル基盤の構築

**なぜやるか？**
- 既存DBのカラムだけでは作戦の幅が限られる
- 累積統計、組み合わせ統計があれば、新しい作戦アイデアが生まれる
- 作戦実装時に毎回SQLを書くのは非効率

**何を作るか？**
- 18個の統計テーブル（.claude/database/stats_tables_design.md参照）
  - 累積成績（馬・騎手・調教師）
  - 組み合わせ統計（馬×騎手、馬×馬場など）
  - 条件別統計（距離適性、枠番成績など）
  - 時間統計（季節別、休養効果など）

**活用例:**
```
作戦A「相性重視」→ stat_horse_jockey_combo を使う
作戦B「条件スペシャリスト」→ stat_horse_track_condition + stat_horse_distance_category を使う
```

### 2. 複数の予想作戦を実装

**作戦 = 仮説 + アルゴリズム**

各作戦は独立したアプローチで、異なる仮説に基づく。

#### 実装済み作戦

**basic-win-prob（王道）**
- 仮説: 各馬の勝率を予測すれば3連単も当たる
- 手法: LightGBM二値分類
- リスク: クラス不均衡（1/8）、3連単の組み合わせ爆発

#### 未実装作戦（優先度順）

**1. learning-to-rank（順位予想）** - 優先度: 高
- 仮説: レース内での順位を直接予測すべき
- 手法: LambdaMART / LambdaRank
- 期待: 3連単予想に最適化されたアプローチ
- なぜ優先: 勝率予測より理論的に正しい

**2. odds-value-hunter（穴馬ハンター）** - 優先度: 高
- 仮説: オッズと実力の乖離を突く
- 手法: オッズバイアス分析
- 期待: 高配当を狙える
- なぜ優先: 収益性の向上

**3. combo-affinity（相性重視）** - 優先度: 中
- 仮説: 馬×騎手の相性が重要
- 手法: stat_horse_jockey_combo を活用
- 期待: 安定した的中率

**4. condition-specialist（条件スペシャリスト）** - 優先度: 中
- 仮説: 馬場・距離適性が決定的
- 手法: 条件別統計を組み合わせ
- 期待: 条件が合った時の高精度

**5. pace-scenario（展開予想型）** - 優先度: 低
- 仮説: レース展開を予測して脚質選択
- 手法: 脚質統計 + ペース分析
- 期待: 上級者向けの戦略
- なぜ低優先: データ不足（コーナー通過順はあるが脚質判定は未実装）

### 3. オッズあり/なしの実験

**核心的な問い: オッズは使うべきか？**

#### パターンA: オッズ完全無視型
- 哲学: AIは「大穴」を知らない。客観的データのみで予想
- メリット: 人間のバイアスに影響されない、過小評価馬を発見
- デメリット: 人間の集合知を捨てている

#### パターンB: オッズ考慮型
- 哲学: 人間の予想には合理性がある
- メリット: 集合知を活用、回収率向上の可能性
- デメリット: 人間のバイアスに引きずられる

#### 実験方法
各作戦でオッズあり/なしの2バージョンを作成し、比較する。

例:
- `learning-to-rank-no-odds`
- `learning-to-rank-with-odds`

### 4. 作戦の評価と比較

**評価指標:**
1. 的中率（3連単）
2. 回収率（投資額に対する回収額）
3. 予想の独自性（オッズとの相関）
4. 大穴発見率（オッズ高配当の的中回数）
5. 安定性（標準偏差）

**比較方法:**
- 時系列交差検証（.claude/analysis/prediction.md参照）
- 過去データで各作戦を検証
- 作戦間の性能比較表を作成

---

## 作戦管理フレームワーク

### ディレクトリ構造

```
.claude/strategies/
  {strategy_id}/
    metadata.yaml      # 作戦メタデータ（仮説、アルゴリズム、リスク）
    README.md          # 説明文書
    implementation.md  # 実装詳細（オプション）
```

### metadata.yamlの構造

```yaml
strategy_id: "learning-to-rank"
display_name: "順位予想型"
display_name_en: "Learning to Rank"
version: "1.0.0"

hypothesis:
  title: "順位を直接予測する"
  description: |
    勝率予測ではなく、レース内での順位を直接予測することで
    3連単の精度を向上させる。
  assumptions:
    - 順位情報は勝率より3連単予想に適している
    - ランキング学習で馬同士の相対関係を学習できる

algorithm:
  type: "ranking"
  models:
    - name: "LambdaMART"
      purpose: "順位予測"
      features:
        - (basic-win-probと同様の特徴量)
      target: "rank (1, 2, 3, ...)"

priority: "high"
status: "planned"  # planned | implementing | implemented | tested | production
last_updated: "2025-11-15"

performance:
  experiments: []
  best_metrics: null

risks:
  - issue: "学習データの準備が複雑"
    severity: "medium"
    mitigation: "LightGBM Rankerを使用"

next_steps:
  - "LightGBM Ranker実装"
  - "時系列検証"
  - "basic-win-probと比較"
```

---

## 実装の流れ

### ステップ1: 統計テーブル構築（1週間）

```bash
# 既存の6テーブルを構築
cd backend
uv run python build_stats_tables.py --drop

# 結果確認
sqlite3 data/kanazawa_dirt_one_spear.db "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stat_%'"
```

### ステップ2: 第1作戦実装（王道の完成）（1週間）

```bash
# GPU環境で訓練
cd analysis
uv run python train_lightgbm.py

# 評価
uv run python evaluate_model.py --model basic-win-prob
```

### ステップ3: 第2作戦実装（Learning to Rank）（2週間）

1. LightGBM Rankerの学習スクリプト作成
2. 時系列交差検証
3. basic-win-probと比較

### ステップ4: 第3作戦実装（Odds Value Hunter）（2週間）

1. オッズバイアス分析スクリプト
2. 過小評価馬の検出ロジック
3. 評価

### ステップ5: 作戦比較レポート作成（1週間）

- 全作戦の性能比較表
- 各作戦の強み・弱みの分析
- 最終的な採用作戦の決定

---

## 追加データ取得（並行作業）

優先度高：
1. 騎手マスターデータのパース（生年月日、読み仮名）
2. 血統データのパース（レース結果HTMLから）
3. 最終オッズの取得戦略決定

優先度中：
4. コース詳細情報の調査

---

## Phase 2完了の定義

以下が達成されたらPhase 2完了：

✅ 統計テーブル（最低6個）が構築済み
✅ 3つ以上の作戦が実装・評価済み
✅ 各作戦の性能比較レポートが完成
✅ 本番運用する作戦（1〜2個）が決定
✅ 時系列検証で実戦精度が推定済み

---

## 次のフェーズへ

**Phase 3: フロントエンド実装**
- 選択された作戦を表示するUI
- 予想の根拠を説明する機能
- 購入結果の記録機能

**Phase 4: 本番運用**
- 毎週の予想開始
- 結果追跡
- 継続的改善

---

## 重要な原則

### 1. すべて記録する
- 失敗した作戦も記録
- なぜダメだったかを文書化
- 試行錯誤もコンテンツ

### 2. 段階的に進める
- 一度に全部やらない
- 1作戦ずつ実装・評価
- 小さく始めて改善

### 3. 比較を楽しむ
- どの作戦が勝つか誰にもわからない
- それを実験するのがPhase 2
- 結果はすべて学び

---

**最終更新**: 2025-11-15
**次のアクション**: 統計テーブル構築 → 第1作戦完成 → 第2作戦実装
