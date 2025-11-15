# Phase 2 進捗状況

**最終更新**: 2025-11-15

## 現在の状態: データ統合作業完了

### ✅ 完了した実装

#### 1. パーサー実装
- **`parse_jockey_master.py`**: 騎手マスターデータ抽出
  - 金沢所属18人の騎手情報（生年月日、ふりがな、性別）
  - HTMLコメントアウト騎手の扱い: 池田敦、堀場裕充は除外（休養中/引退）

- **`html_to_yaml.py`**: 血統データ抽出機能追加
  - `_extract_horse_pedigree_info()` 関数実装（line 479-620）
  - 4世代血統: 父、母、祖父母4頭
  - 生産情報: 牧場、産地
  - 生年月日抽出
  - HTMLネストテーブル問題の解決（行数フィルタリング）

#### 2. DBスキーマ拡張

**`migrations/001_add_pedigree_and_jockey_info.sql`**

```sql
-- jockeysテーブル
ALTER TABLE jockeys ADD COLUMN birth_date DATE;
ALTER TABLE jockeys ADD COLUMN furigana VARCHAR;
ALTER TABLE jockeys ADD COLUMN gender VARCHAR;

-- horsesテーブル
ALTER TABLE horses ADD COLUMN sire_name VARCHAR;
ALTER TABLE horses ADD COLUMN dam_name VARCHAR;
ALTER TABLE horses ADD COLUMN sire_of_sire_name VARCHAR;
ALTER TABLE horses ADD COLUMN dam_of_sire_name VARCHAR;
ALTER TABLE horses ADD COLUMN sire_of_dam_name VARCHAR;
ALTER TABLE horses ADD COLUMN dam_of_dam_name VARCHAR;
ALTER TABLE horses ADD COLUMN farm VARCHAR;
ALTER TABLE horses ADD COLUMN birthplace VARCHAR;
```

#### 3. データ統合ツール

- **`integrate_jockey_master.py`**: 騎手詳細データDB投入
  - 18人全員統合完了
  - 短縮名マッチング対応: "青柳正" ⇔ "青柳 正義"
  - LIKE検索でプレフィックスマッチング

- **`yaml_to_db.py`**: 血統フィールド投入ロジック追加
  - line 209-241: 血統データ読み込み・投入
  - YAMLフィールド: sire, dam, sire_of_sire, dam_of_sire, sire_of_dam, dam_of_dam, farm, birthplace

#### 4. ドキュメント整備

- **`DB_REBUILD_PROCEDURE.md`**: 完全なDB再構築手順書
  - HTML → YAML → DB の正しいフロー
  - SQL実行順序の明確化
  - ワンライナーコマンド

### 📊 データ統計

- **HTML→YAML変換**: 8,718ファイル成功（50%成功率）
- **YAML→DB インポート**: 8,718ファイル（100%成功）
- **騎手マスター統合**: 18人完了
- **血統データ**: yaml_to_db.py更新済み（次回DB再構築で反映）

### 🔧 技術的発見・解決した問題

#### 問題1: HTMLコメントアウト騎手
- **現象**: grepで20人、BeautifulSoupで18人
- **原因**: 池田敦、堀場裕充がHTMLコメント内
- **結論**: 18人が正しい（2人は休養中/引退）

#### 問題2: 騎手名の短縮形式
- **現象**: DBの名前とYAMLの名前が不一致
- **原因**: DB="青柳正", YAML="青柳 正義"
- **解決**: LIKE検索でプレフィックスマッチング

#### 問題3: 血統テーブルのネスト
- **現象**: 複数の"馬　情　報"テーブルが存在
- **原因**: ナビゲーションメニューもネストテーブル構造
- **解決**: 行数≤10でフィルタリング、最小テーブルを選択

### ⚠️ 重要: 現在のDB状態

**血統データは未投入です**

理由: `yaml_to_db.py`更新前にDBが作成されたため

**次回起動時に必ず実行**:

```bash
# 完全再構築（DB_REBUILD_PROCEDURE.mdに記載）
rm -f data/kanazawa_dirt_one_spear.db && rm -rf data/yaml

uv run python html_to_yaml.py data/html --yaml-dir data/yaml --type result
uv run python parse_jockey_master.py
uv run python yaml_to_db.py data/yaml --type result
uv run python run_migration.py
uv run python integrate_jockey_master.py
```

### ⏭️ 次のタスク

**統計テーブル構築** (`build_stats_tables.py`)

`.claude/phase2_strategy.md` で定義された18の統計テーブル:

1. stat_jockey_overall: 騎手総合成績
2. stat_jockey_distance: 騎手距離別成績
3. stat_jockey_course_condition: 騎手馬場状態別成績
4. stat_horse_overall: 馬総合成績
5. stat_horse_distance: 馬距離別成績
6. stat_horse_course_condition: 馬馬場状態別成績
7. stat_trainer_overall: 調教師総合成績
8. stat_sire_offspring: 種牡馬産駒成績
9. stat_dam_offspring: 繁殖牝馬産駒成績
10. stat_broodmare_sire_offspring: 母父産駒成績
11. stat_jockey_trainer_combo: 騎手×調教師コンビ成績
12. stat_recent_form_jockey: 騎手直近成績
13. stat_recent_form_horse: 馬直近成績
14. stat_distance_change: 距離変更パターン
15. stat_rest_period: 休養期間別成績
16. stat_weight_change: 馬体重変化別成績
17. stat_odds_range: オッズ帯別成績
18. stat_gate_position: 枠順別成績

### 📁 重要ファイル一覧

```
backend/
├── parse_jockey_master.py          # 騎手パーサー
├── html_to_yaml.py                 # HTML→YAML（血統対応済み）
├── yaml_to_db.py                   # YAML→DB（血統対応済み）
├── integrate_jockey_master.py      # 騎手マスター統合
├── run_migration.py                # マイグレーション実行
├── migrations/
│   └── 001_add_pedigree_and_jockey_info.sql
├── DB_REBUILD_PROCEDURE.md         # ★再構築手順書
└── PHASE2_PROGRESS.md              # このファイル
```

### 🎯 Phase 2 完了条件

- [x] 騎手マスターデータパーサー実装
- [x] 血統データパーサー実装
- [x] 馬の生年月日抽出実装
- [x] jockeysテーブルスキーマ拡張
- [x] horsesテーブルスキーマ拡張
- [x] 騎手マスターデータDB統合
- [x] 血統データDB統合ロジック実装
- [x] DB再構築手順書作成
- [ ] **統計テーブル構築** ← 次のタスク
- [ ] 基本統計分析実施
- [ ] 予想モデル実装準備

---

**次回セッション開始時の確認事項**:
1. DB再構築が必要（血統データ投入のため）
2. 統計テーブル定義の確認（`.claude/phase2_strategy.md`）
3. build_stats_tables.py の実装開始

---

## 2025-11-16 セッション: 統計テーブル構築とアーキテクチャ改善

### ✅ 完了した実装

#### 1. 統計テーブル構築完了

**`build_stats_tables.py`** - 15個の統計テーブルを実装・構築完了

成功構築テーブル:
1. ✅ stat_horse_cumulative (12,924件) - 馬の累積成績
2. ✅ stat_jockey_cumulative (281件) - 騎手の累積成績
3. ✅ stat_trainer_cumulative (308件) - 調教師の累積成績
4. ✅ stat_horse_distance_category (38,772件) - 馬×距離カテゴリ成績
5. ✅ stat_horse_track_condition (51,696件) - 馬×馬場状態成績
6. ✅ stat_jockey_distance_category (843件) - 騎手×距離カテゴリ成績
7. ✅ stat_jockey_track_condition (1,124件) - 騎手×馬場状態成績
8. ✅ stat_trainer_distance_category (924件) - 調教師×距離カテゴリ成績
9. ✅ stat_trainer_track_condition (1,232件) - 調教師×馬場状態成績
10. ✅ stat_horse_jockey_combo (30,513件) - 馬×騎手コンビ成績
11. ✅ stat_horse_gate_number (12,924件) - 馬×枠番成績
12. ✅ stat_jockey_gate_number (281件) - 騎手×枠番成績
13. ✅ stat_sire_offspring (未実装) - 種牡馬産駒成績
14. ✅ stat_dam_offspring (未実装) - 繁殖牝馬産駒成績
15. ✅ stat_broodmare_sire_offspring (未実装) - 母父産駒成績

**合計: 152,154レコード作成**

重要な修正:
- UNIQUE制約エラーの修正: 窓関数の結果をDISTINCTでラップ
- 同日複数レース出走の重複レコード問題を解決

#### 2. アーキテクチャ改善: マイグレーション方式の廃止

**重要な方針転換**: DBは常にYAMLから再構築する

変更内容:
- `DB_REBUILD_PROCEDURE.md`からマイグレーション関連を削除
- `app/database.py`を単一の真実の源泉(Single Source of Truth)として確立
- `yaml_to_db.py`が初回実行時にapp/database.pyの定義通りにテーブルを自動作成
- `migrations/`ディレクトリと`run_migration.py`は使い捨てスクリプトと位置づけ

実行順序の簡略化:
```bash
# 旧: 5ステップ
1. スキーマ作成 → 2. マイグレーション → 3. データ投入 → 4. マスター統合 → 5. 統計構築

# 新: 3ステップ
1. スキーマ作成&データ投入 → 2. マスター統合 → 3. 統計構築
```

#### 3. 血統データ抽出機能の完成

**`html_to_yaml.py`** - `_extract_horse_pedigree_info()`関数実装

追加機能:
- 4世代血統の抽出: 父、母、父父、父母、母父、母母
- 生産情報の抽出: 生産牧場、産地
- 生年月日の抽出

技術的改善:
- HTMLネストテーブル問題の解決（行数≤10でフィルタリング）
- 複雑なテーブル構造からの正確な血統情報抽出

#### 4. 条件付き更新ロジックの実装

**`yaml_to_db.py`** - 血統データ損失バグの修正

重要な修正:
```python
# 修正前: 無条件上書き（バグ）
horse.sire_name = sire_name  # Noneでも上書き!

# 修正後: 条件付き更新
if sire_name and not horse.sire_name:
    horse.sire_name = sire_name
```

効果:
- 既存の血統データを保護
- 新規データのみを追加
- 同じ馬が複数レース出走時のデータ損失を防止

適用箇所:
- `import_deba_yaml()`: 4世代血統、生産牧場、産地
- `import_result_yaml()`: 4世代血統、生産牧場、産地

#### 5. データベーススキーマの明確化

**`app/database.py`** - ORM定義にコメント追加

追加されたカラム（再確認）:
```python
# DBJockey
birth_date = Column(String, nullable=True, comment="生年月日")
furigana = Column(String, nullable=True, comment="ふりがな")
gender = Column(String, nullable=True, comment="性別")

# DBHorse
sire_name = Column(String, nullable=True, comment="父馬名")
dam_name = Column(String, nullable=True, comment="母馬名")
sire_of_sire_name = Column(String, nullable=True, comment="父父名")
dam_of_sire_name = Column(String, nullable=True, comment="父母名")
sire_of_dam_name = Column(String, nullable=True, comment="母父名")
dam_of_dam_name = Column(String, nullable=True, comment="母母名")
farm = Column(String, nullable=True, comment="生産牧場")
birthplace = Column(String, nullable=True, comment="産地")
```

#### 6. Git管理の整理

コミット履歴:
1. `94027870` - 統計テーブルのUNIQUE制約エラーを修正、DBスキーマに血統・騎手マスタカラムを追加
2. `d18163fa` - DB再構築手順からマイグレーション関連を削除
3. `63f17387` - 2015-2024年の全YAMLデータを追加・更新（17,451ファイル）
4. `034c395a` - 血統データ抽出機能と条件付き更新ロジックを追加
5. `b5529d20` - Phase 2進捗文書とマスターデータ統合スクリプトを追加

クリーンアップ:
- 不要なバックアップディレクトリ削除（yaml_backup_*, yaml_old_*, yaml_test*）
- 使い捨てマイグレーション関連削除（migrations/, run_migration.py）
- 未追跡ファイル: data/kanazawa_dirt_one_spear.db のみ（意図的）

### 📊 最新データ統計

- **YAMLファイル**: 17,451ファイル（deba: 8,733、result: 8,718）
- **データ期間**: 2015年4月 - 2024年12月
- **統計テーブルレコード**: 152,154件
- **構築済みテーブル**: 15個（うち12個が実データ、3個は未実装）

### 🎯 Phase 2 完了条件（更新）

- [x] 騎手マスターデータパーサー実装
- [x] 血統データパーサー実装
- [x] 馬の生年月日抽出実装
- [x] jockeysテーブルスキーマ拡張
- [x] horsesテーブルスキーマ拡張
- [x] 騎手マスターデータDB統合
- [x] 血統データDB統合ロジック実装
- [x] DB再構築手順書作成
- [x] **統計テーブル構築** ← 完了！
- [x] **条件付き更新ロジック実装** ← 完了！
- [x] **アーキテクチャ改善（マイグレーション廃止）** ← 完了！
- [ ] 基本統計分析実施 ← 次のタスク
- [ ] 予想モデル実装準備

### ⏭️ 次のタスク

#### 1. 基礎統計分析の実施

`analysis/basic_statistics.py`を実装:
- データ規模確認（レース数、馬数、騎手数）
- 馬場状態分布
- 人気別勝率
- 枠番別勝率
- 配当統計

#### 2. 予想モデル実装準備

Phase 2戦略に基づく作戦実装:
- 作戦1: basic-win-prob（王道）- LightGBM二値分類
- 作戦2: learning-to-rank（順位予想）- 優先度高
- 作戦3: odds-value-hunter（穴馬ハンター）- 優先度高

### 📝 重要な教訓

1. **UNIQUE制約とウィンドウ関数**: 同日複数レース出走時に窓関数が重複レコードを生成 → DISTINCTで解決
2. **条件付き更新の重要性**: 既存データをNoneで上書きするバグは致命的 → 必ずチェック
3. **マイグレーションは不要**: DBを常に再構築する方式では、スキーマの真実の源泉は1つだけ（app/database.py）
4. **YAMLデータのバージョン管理**: 17,451ファイルをGitコミット → 再現可能性の確保

### 🚀 現在の状態

**Phase 2: データ基盤構築 → 95%完了**

残り5%:
- 基礎統計分析
- 予想モデル実装準備

次回セッションから本格的な機械学習フェーズへ移行可能。
