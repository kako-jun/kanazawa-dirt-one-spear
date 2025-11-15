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
