# データパイプライン・アーキテクチャ

**最終更新**: 2025-11-20
**重要度**: ★★★★★（全開発者必読）

---

## 1. 基本方針

### 成果物の定義

#### ✅ コミット対象（ソースコードのみ）

**Pythonスクリプト・設定ファイル**

```
backend/
├── *.py              # 全Pythonスクリプト
├── pyproject.toml    # 依存関係
└── app/             # FastAPIアプリ

analysis/
└── *.py              # 分析スクリプト

.claude/
└── **/*.md           # ドキュメント
```

#### ⚠️ コミット対象外（リリースページに添付 or ローカル生成）

**1. データベース（各自がローカルで構築 or リリース添付）**

```
kanazawa_dirt_one_spear.db
├── 生データ層（頻繁には変更しない）
│   ├── races              # レース基本情報
│   ├── horses             # 馬マスター
│   ├── jockeys            # 騎手マスター
│   ├── trainers           # 調教師マスター
│   ├── entries            # 出走エントリ
│   ├── race_performances  # 個別成績
│   └── payouts            # 配当情報
│
└── 統計層（気軽に削除・再構築可能）
    ├── stat_horse_cumulative       # 馬の累積成績
    ├── stat_jockey_cumulative      # 騎手の累積成績
    ├── stat_trainer_cumulative     # 調教師の累積成績
    ├── stat_horse_distance_category
    ├── stat_horse_track_condition
    ├── stat_horse_jockey_combo
    └── ... (その他 stat_* テーブル)
```

**配布方法**:
- Gitリリースページにアップロード
- または各自がYAML→DBを実行

**2. 訓練済みモデル（Gitコミット + リリースページ）**

```
analysis/output/models/
├── lightgbm_no_odds.pkl      # オッズなしモデル (258KB)
├── lightgbm_with_odds.pkl    # オッズありモデル (284KB)
├── model_comparison.csv      # 性能比較レポート
├── training_report_*.md      # 訓練レポート
└── feature_importance_*.*    # 特徴量重要度
```

**配布方法**:
- **軽量モデル（<1MB）はGitコミット対象** - トレーサビリティ確保のため
- 大型モデル（>10MB）はGitリリースページにアップロード
- 現状：全てのモデルが1MB未満のためコミット

**3. 特徴量CSV（副産物・検証用）**

```
analysis/output/features/
└── features.csv  # 検証・デバッグ用（完全にローカルのみ）
```

**配布不要**:
- DBから再生成可能
- 開発者のローカル環境でのみ使用

**役割**:
- 統計テーブル → CSV 変換時のミスを確認
- 目視でデータを検証
- モデル訓練の入力として使用

**なぜコミット不要？**
- DBから再生成可能
- サイズが大きい（24MB+）
- 中間ファイルでしかない

---

## 2. データフロー

### 全体像

```
┌─────────────────────────────────────────────────────┐
│ Phase 1: データ収集                                  │
├─────────────────────────────────────────────────────┤
│ HTML → YAML → DB（生データ層）                       │
│                                                     │
│ html_to_yaml.py                                     │
│     ↓                                               │
│ yaml_to_db.py                                       │
│     ↓                                               │
│ races, horses, jockeys, race_performances, payouts  │
└─────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────┐
│ Phase 2-1: 統計テーブル構築                          │
├─────────────────────────────────────────────────────┤
│ 生データ層 → 統計層（stat_*テーブル）                │
│                                                     │
│ build_stats_tables.py                               │
│     ↓                                               │
│ stat_horse_cumulative                               │
│ stat_jockey_cumulative                              │
│ stat_trainer_cumulative                             │
│ ... (15テーブル)                                     │
└─────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────┐
│ Phase 2-2: 特徴量生成                                │
├─────────────────────────────────────────────────────┤
│ 統計層 → CSV（検証用）                               │
│                                                     │
│ feature_engineering_v2.py                           │
│     ↓                                               │
│ features.csv （コミット対象外）                       │
│                                                     │
│ 【重要】統計テーブルから特徴量を取得                  │
│ その場計算はしない！                                 │
└─────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────┐
│ Phase 2-3: モデル訓練                                │
├─────────────────────────────────────────────────────┤
│ CSV → 訓練済みモデル                                 │
│                                                     │
│ train_lightgbm.py                                   │
│     ↓                                               │
│ lightgbm_no_odds.pkl                                │
│ lightgbm_with_odds.pkl                              │
│ model_comparison.csv                                │
└─────────────────────────────────────────────────────┘
```

---

## 3. 統計テーブルの管理

### 3.1 統計テーブルの削除・再構築

**問題**: 統計計算にミスがあった場合、全DBを作り直すのは時間がかかる（数十分）

**解決策**: 統計テーブル（`stat_*`）だけを削除・再構築

#### 削除手順

```bash
# 方法1: 個別削除
sqlite3 data/kanazawa_dirt_one_spear.db "
DELETE FROM stat_horse_cumulative;
DELETE FROM stat_jockey_cumulative;
DELETE FROM stat_trainer_cumulative;
-- 必要に応じて他のテーブルも
"

# 方法2: 全stat_*テーブルをDROP（推奨）
sqlite3 data/kanazawa_dirt_one_spear.db "
SELECT 'DROP TABLE IF EXISTS ' || name || ';'
FROM sqlite_master
WHERE type='table' AND name LIKE 'stat_%';
" | sqlite3 data/kanazawa_dirt_one_spear.db
```

#### 再構築

```bash
cd backend
uv run python build_stats_tables.py
```

**所要時間**: 約1-2分（全DB再構築は数十分）

### 3.2 利点

✅ **生データは保護される**
- YAML→DB変換（長時間）を再実行不要

✅ **統計層だけ何度でも試行錯誤できる**
- 計算式の変更
- 新しい統計テーブルの追加
- バグ修正

✅ **開発速度の向上**
- 1-2分で統計テーブルを作り直せる
- 失敗を恐れずに実験できる

---

## 4. 各スクリプトの責務

### 4.1 `html_to_yaml.py`

**責務**: HTML → YAML変換

**入力**: `data/html/YYYY/YYYYMMDD/race_*.html`

**出力**: `data/yaml/YYYY/YYYYMMDD/race_*.yaml`

**実行頻度**: データ収集時のみ（週1回程度）

---

### 4.2 `yaml_to_db.py`

**責務**: YAML → DB（生データ層）投入

**入力**: `data/yaml/`

**出力**:
- `races`, `horses`, `jockeys`, `trainers`
- `entries`, `race_performances`, `payouts`

**実行頻度**: DB初期構築 or 新データ追加時

---

### 4.3 `build_stats_tables.py`

**責務**: 生データ層 → 統計層構築

**入力**: `race_performances`, `races`, etc.

**出力**:
- `stat_horse_cumulative`
- `stat_jockey_cumulative`
- `stat_trainer_cumulative`
- その他15テーブル

**実行頻度**:
- 統計テーブル構築時
- 統計計算修正時（頻繁）

**重要**:
- **このスクリプトが統計層の唯一の作成者**
- 他のスクリプトは統計テーブルを参照するのみ

---

### 4.4 `feature_engineering_v2.py`

**責務**: 統計層 → 特徴量CSV生成

**入力**:
- `race_performances`（基本情報）
- `stat_horse_cumulative`（馬の統計）
- `stat_jockey_cumulative`（騎手の統計）
- `stat_trainer_cumulative`（調教師の統計）
- その他 `stat_*` テーブル

**出力**: `analysis/output/features/features.csv`

**重要**:
- ❌ **その場計算は禁止**
- ✅ **統計テーブルからJOINで取得**

**例（悪い実装）**:
```python
# ❌ ダメな例
df['horse_win_rate'] = grouped['win'].cumsum().shift(1) / grouped.cumcount()
```

**例（良い実装）**:
```python
# ✅ 正しい例
query = """
SELECT
    rp.*,
    hc.win_rate as horse_win_rate,
    hc.place_rate as horse_place_rate,
    hc.avg_finish_position as horse_avg_finish
FROM race_performances rp
LEFT JOIN stat_horse_cumulative hc
    ON rp.horse_id = hc.horse_id
"""
```

---

### 4.5 `train_lightgbm.py`

**責務**: CSV → 訓練済みモデル

**入力**: `analysis/output/features/features.csv`

**出力**:
- `lightgbm_no_odds.pkl`
- `lightgbm_with_odds.pkl`
- `model_comparison.csv`
- `feature_importance_*.png`

**実行頻度**:
- 特徴量変更時
- ハイパーパラメータ調整時

---

## 5. よくある質問

### Q1: なぜCSVをコミットしないのか？

**A**:
- DBから再生成可能（ `feature_engineering_v2.py` 実行）
- サイズが大きい（24MB+）
- 中間ファイルでしかない
- Gitで差分管理する必要がない

### Q2: 統計テーブル構築が遅い場合は？

**A**:
- インデックスを追加（`race_performances.horse_id`, `race_performances.race_id`）
- ウィンドウ関数の最適化
- 並列処理の導入

### Q3: 統計テーブルの計算式を変更したい

**A**:
```bash
# 1. 統計テーブル削除
sqlite3 data/kanazawa_dirt_one_spear.db "
SELECT 'DROP TABLE IF EXISTS ' || name || ';'
FROM sqlite_master
WHERE type='table' AND name LIKE 'stat_%';
" | sqlite3 data/kanazawa_dirt_one_spear.db

# 2. build_stats_tables.py を修正

# 3. 再構築
uv run python build_stats_tables.py

# 4. 特徴量CSV再生成
uv run python ../analysis/feature_engineering_v2.py

# 5. モデル再訓練
uv run python ../analysis/train_lightgbm.py
```

### Q4: 生データを更新したい（新しいYAMLを追加）

**A**:
```bash
# 1. YAMLをDBに追加投入
uv run python yaml_to_db.py data/yaml --type result

# 2. 統計テーブル再構築
# （方法1）全削除→再構築
sqlite3 data/kanazawa_dirt_one_spear.db "
SELECT 'DROP TABLE IF EXISTS ' || name || ';'
FROM sqlite_master
WHERE type='table' AND name LIKE 'stat_%';
" | sqlite3 data/kanazawa_dirt_one_spear.db

uv run python build_stats_tables.py

# 3. 以降の手順は Q3 と同じ
```

---

## 6. .gitignoreの設定

```gitignore
# データベース（リリースページに添付）
backend/data/*.db
backend/data/*.sqlite
backend/data/*.sqlite3

# YAML生データ（リリースページに添付 or 各自がスクレイピング）
backend/data/yaml/

# 中間ファイル（CSVなど）
analysis/output/features/*.csv

# 大型モデルのみ除外（現状は全て<1MBなのでコミット対象）
# analysis/output/models/*.pkl  # コメントアウト：軽量なのでコミット
```

**Gitコミット対象**:
1. `analysis/output/models/*.pkl` - 訓練済みモデル（軽量：<1MB）
2. `analysis/output/models/*.csv` - 性能比較レポート
3. `analysis/output/models/*.md` - 訓練レポート
4. `analysis/output/models/*.png` - 特徴量重要度図（日本語フォント警告あるが保存）

**リリースページでの配布**（将来的に必要な場合）:
1. `kanazawa_dirt_one_spear.db` - データベース本体（大容量）
2. 大型モデル（>10MB）がある場合

**方針**:
- **トレーサビリティ重視** - 作戦の経過をフロントエンドで発表するため全記録
- 軽量ファイル（<1MB）はGitコミット
- 大容量ファイル（>10MB）のみリリースページ

---

## 7. まとめ

### データ層の構造

```
生データ層（YAML→DB、頻繁変更なし）
    ↓
統計層（気軽に削除・再構築可能）
    ↓
CSV（検証用、コミット対象外）
    ↓
モデル（訓練済み、コミット対象）
```

### 重要原則

1. **統計テーブルは気軽に作り直せる**
   - `stat_*` プレフィクスで識別
   - DROP → 再構築が1-2分

2. **CSVはコミット対象外**
   - DBから再生成可能
   - 検証・デバッグ用のみ

3. **その場計算は禁止**
   - `feature_engineering_v2.py`は統計テーブルを参照
   - 累積統計を再計算しない

4. **生データ層は保護する**
   - 統計層の試行錯誤で影響を受けない
   - YAML→DB変換を頻繁に実行しない

---

**このドキュメントを全開発者が理解することで、データパイプラインの混乱を防ぎます。**
