# データベース再構築手順

## 基本方針

**DBは常にYAMLから構築する**

- HTML → YAML → DB の一方向フロー
- DBを丸ごと削除して作り直すのが基本
- 再現可能性を重視

## 完全再構築手順

### 1. 前準備: HTMLファイルが存在することを確認

```bash
ls data/html/2024/  # レース結果HTML
ls data/reference_data/html/guide/  # マスターデータHTML
```

### 2. 既存DBとYAMLを削除（クリーンスタート）

```bash
rm -f data/kanazawa_dirt_one_spear.db
rm -rf data/yaml
```

### 3. HTML → YAML 変換

#### 3-1. レース結果データ

```bash
uv run python html_to_yaml.py data/html --yaml-dir data/yaml --type result
```

- 入力: `data/html/**/*_result.html`
- 出力: `data/yaml/result/**/*.yaml`
- 含まれるデータ:
  - レース基本情報
  - 出走馬情報
  - 着順・タイム
  - **血統情報**（父、母、祖父母4頭）
  - **馬の生年月日、生産牧場、産地**
  - オッズ・払戻金

#### 3-2. 出馬表データ

```bash
uv run python html_to_yaml.py data/html --yaml-dir data/yaml --type deba
```

- 入力: `data/html/**/*_deba.html`
- 出力: `data/yaml/deba/**/*.yaml`
- 含まれるデータ:
  - レース基本情報
  - 出走予定馬情報

#### 3-3. マスターデータ（騎手）

```bash
uv run python parse_jockey_master.py
```

- 入力: `data/reference_data/html/guide/jockeys_kanazawa.html`
- 出力: `data/reference_data/yaml/master/jockeys_kanazawa.yaml`
- 含まれるデータ:
  - 騎手名、ふりがな
  - 生年月日、性別
  - 騎手免許番号

### 4. YAML → DB インポート

**DBファイル初期化**: yaml_to_db.py が初回実行時に app/database.py の定義に基づいてテーブルを自動作成

**⚠️ 重要: 必ず deba → result の順で実行すること**

理由:
- **deba（出馬表）**: レース詳細情報（レース名、距離、賞金など）を含む
- **result（結果）**: 馬場状態、天候、成績データのみ
- deba を先にインポートすることで、レース基本情報が先に登録され、result で詳細を追加できる

#### 4-1. 出馬表データ（先に実行）

```bash
uv run python yaml_to_db.py data/yaml --type deba
```

- 読み込み: `data/yaml/deba/**/*.yaml`
- 投入先テーブル:
  - **races** ← レース詳細情報（レース名、距離、賞金など）
  - horses
  - jockeys
  - trainers
  - race_entries

#### 4-2. レース結果データ（後に実行）

```bash
uv run python yaml_to_db.py data/yaml --type result
```

- 読み込み: `data/yaml/result/**/*.yaml`
- 投入先テーブル:
  - races ← 馬場状態・天候を更新
  - horses（血統情報含む）
  - jockeys
  - trainers
  - race_entries
  - race_results
  - odds（オッズ情報）
  - payouts（払戻情報）

### 5. マスターデータ統合

#### 5-1. 騎手マスターデータ

```bash
uv run python integrate_jockey_master.py
```

- YAMLから騎手の詳細情報（生年月日、ふりがな、性別）を既存のjockeysレコードに追加
- 名前照合: 短縮名対応（DB: "青柳正" ⇔ YAML: "青柳 正義"）

### 6. 統計テーブル構築

```bash
uv run python build_stats_tables.py
```

- Phase 2 で定義される18の統計テーブルを構築
- 騎手・馬・コース別の集計データ

## 実行順序の整理

### 推奨順序

1. **スキーマ作成 & データ投入** (yaml_to_db.py)
   - app/database.py の定義に基づきテーブルを自動作成
   - deba → result の順でデータをインポート

2. **マスターデータ統合** (integrate_jockey_master.py)
   - 既存レコードの UPDATE

3. **統計テーブル構築** (build_stats_tables.py)
   - 集計用テーブル作成

## ワンライナーでの完全再構築

```bash
# 1. クリーンアップ
rm -f data/kanazawa_dirt_one_spear.db && rm -rf data/yaml

# 2. HTML → YAML
uv run python html_to_yaml.py data/html --yaml-dir data/yaml --type result && \
uv run python html_to_yaml.py data/html --yaml-dir data/yaml --type deba && \
uv run python parse_jockey_master.py

# 3. YAML → DB (スキーマ自動作成 & データ投入)
# ⚠️ 重要: deba → result の順で実行（レース詳細を先に登録）
uv run python yaml_to_db.py data/yaml --type deba && \
uv run python yaml_to_db.py data/yaml --type result

# 4. マスターデータ統合
uv run python integrate_jockey_master.py

# 5. 統計テーブル構築
uv run python build_stats_tables.py
```

## 注意事項

- **スキーマの真実の源泉**: app/database.py がすべて。yaml_to_db.py 初回実行時にこの定義通りにテーブル作成
- **冪等性**: html_to_yaml.py は既存YAMLを上書き
- **データ整合性**: DBを部分的に更新せず、常に全体を再構築
- **バックアップ**: 本番運用時は再構築前にDBバックアップを推奨

## 重要なバグ修正履歴

### 2025-11-15: 血統データ損失バグ修正

**問題**: import_deba_yaml関数が血統情報を無条件上書きし、Noneで既存データを消去

**症状**:
- 同じ馬が複数レースに出走した場合、2回目以降のインポートで血統データがNullに
- 結果として血統カバー率が55%-70%に留まる

**根本原因** (yaml_to_db.py:233-241):
```python
# バグのあるコード
horse.sire_name = sire_name  # ← Noneでも上書き!
horse.dam_name = dam_name
```

**修正内容**:
```python
# 修正後: 条件付き更新
if sire_name and not horse.sire_name:
    horse.sire_name = sire_name
if dam_name and not horse.dam_name:
    horse.dam_name = dam_name
```

**効果**: 修正により血統カバー率がほぼ100%に到達見込み

---

**最終更新**: 2025-11-15 (血統バグ修正版)
