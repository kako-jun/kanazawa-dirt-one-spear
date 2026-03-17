# TODO - 追加実装項目

## Phase 2: データ収集・統計テーブル拡張

### 1. 追加スクレイピング（未実装）

#### 優先度: 高
- [ ] **コース・競馬場マスターデータ**
  - URL: (調査が必要)
  - 取得項目:
    - コース名、距離、形状
    - 直線距離、コーナー数
    - 特徴（内枠有利など）
  - 保存先: `backend/data/yaml/master/courses.yaml`
  - DBテーブル: `courses`

- [ ] **馬齢データ**
  - 現在のrace_performancesに追加可能か調査
  - または馬マスターに生年月日を追加

- [ ] **斤量データ**
  - レース結果ページから取得可能か調査
  - race_performancesテーブルに`weight`カラム追加

#### 優先度: 中
- [ ] **天候データ**
  - 現在: racesテーブルに`weather`カラムはあるが未使用
  - HTMLから抽出して格納

- [ ] **血統データ（もし取得可能なら）**
  - 父馬、母馬、母父
  - 保存先: horsesテーブルに追加
  - DBスキーマ拡張が必要

### 2. 統計テーブル追加実装（未実装）

現在実装済み:
- ✅ stat_horse_cumulative
- ✅ stat_jockey_cumulative
- ✅ stat_trainer_cumulative
- ✅ stat_horse_jockey_combo
- ✅ stat_horse_track_condition
- ✅ stat_popularity_performance

追加実装が必要:
- [ ] **stat_horse_distance_category**: 馬ごとの距離適性
- [ ] **stat_jockey_trainer_combo**: 騎手×調教師の連携統計
- [ ] **stat_gate_position**: 枠番別の成績
- [ ] **stat_horse_number**: 馬番別の成績（オカルト検証）
- [ ] **stat_odds_bias**: 人気と実力の乖離分析
- [ ] **stat_running_style**: 馬の脚質判定
- [ ] **stat_rest_days_effect**: 休養期間の影響
- [ ] **stat_seasonal_performance**: 季節・月別成績
- [ ] **stat_head_to_head**: 馬同士の対戦成績

### 3. build_stats_tables.py の拡張

現在: 6テーブルのみ実装

追加が必要:
- [ ] 上記の未実装統計テーブルを追加
- [ ] 実行時のログ改善
- [ ] エラーハンドリング強化
- [ ] 進捗表示（tqdm等）

---

## Phase 2: 予想作戦の実装

### 作戦フレームワーク

ディレクトリ構造:
```
.claude/strategies/
  {strategy_id}/
    metadata.yaml     # 作戦メタデータ
    README.md         # 説明文書
    implementation.md # 実装詳細
```

### 作戦候補

#### 実装済み
- ✅ **basic-win-prob** (王道): LightGBM二値分類
  - 実装: `analysis/train_lightgbm.py`
  - ステータス: 実装完了、未実行

#### 未実装（優先度順）

1. **learning-to-rank** (順位予想)
   - 手法: LambdaMART / LambdaRank
   - 目的: レース内での順位を直接予測
   - 優先度: 高
   - 期待: 3連単予想に最適

2. **odds-value-hunter** (穴馬ハンター)
   - 手法: オッズバイアス分析
   - 目的: 過小評価されている馬を発見
   - 優先度: 高
   - 期待: 高配当狙い

3. **combo-affinity** (相性重視)
   - 手法: stat_horse_jockey_combo を活用
   - 目的: 相性の良い組み合わせで予想
   - 優先度: 中

4. **condition-specialist** (条件スペシャリスト)
   - 手法: stat_horse_track_condition + stat_horse_distance_category
   - 目的: 条件に合った馬を選択
   - 優先度: 中

5. **pace-scenario** (展開予想型)
   - 手法: stat_running_style + ペース分析
   - 目的: レース展開を予測して有利な脚質を選択
   - 優先度: 低（データ不足）

---

## Phase 3: フロントエンド実装

参照: `.claude/presentation/frontend.md`

### 未実装
- [ ] Next.js セットアップ
- [ ] レトロデザインUI
- [ ] 予想表示機能
- [ ] 購入結果記録機能
- [ ] 統計ダッシュボード

---

## その他

### ドキュメント整備
- [ ] 作戦メタデータスキーマのサンプル作成
- [ ] 統計テーブル設計の完成版ドキュメント
- [ ] API設計（フロントエンド連携用）

### 実験・評価
- [ ] GPU環境で既存モデルの訓練・評価
- [ ] 作戦間の性能比較フレームワーク
- [ ] バックテスト環境の構築

---

**最終更新**: 2025-11-15
**次のステップ**: 統計テーブル構築 → GPU環境でモデル訓練 → 作戦追加実装
