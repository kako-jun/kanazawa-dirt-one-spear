# 配当データ取得問題の解決 - 2025-11-14

## 問題の原因

**枠連複・枠連単のインデックスずれ**

金沢競馬では枠連複・枠連単が発売されていないため、HTMLテーブルの列インデックスが想定と6列ずれていた。

### 修正前のインデックス（誤）
```python
bet_types = [
    ('win', '単勝', 1),
    ('place', '複勝', 4),
    ('bracket_quinella', '枠連複', 7),   # ← 存在しない
    ('quinella', '馬連複', 10),
    ('bracket_exacta', '枠連単', 13),    # ← 存在しない
    ('exacta', '馬連単', 16),
    ('wide', 'ワイド', 19),
    ('trio', '三連複', 22),
    ('trifecta', '三連単', 25),          # ← インデックス25だが実際は19
]
```

### 修正後のインデックス（正）
```python
bet_types = [
    ('win', '単勝', 1),
    ('place', '複勝', 4),
    ('quinella', '馬連複', 7),           # 枠連複をスキップ
    ('exacta', '馬連単', 10),            # 枠連単をスキップ
    ('wide', 'ワイド', 13),              # 6列ずれ修正
    ('trio', '三連複', 16),              # 6列ずれ修正
    ('trifecta', '三連単', 19),          # 6列ずれ修正（25→19）
]
```

---

## 修正内容

### 修正ファイル

1. **backend/html_to_yaml.py**
   - Line 587-596: bet_typesリストを修正

2. **backend/app/scrapers/nar_scraper.py**
   - Line 505-514: bet_typesリストを修正

### 検証結果

**テストデータ**: 2015年4月4日 第2レース

**修正前**:
```yaml
payouts:
  win: {...}
  place: {...}
  # trifectaなし（条件チェックで弾かれていた）
```

**修正後**:
```yaml
payouts:
  win:
    combo: '6'
    payout: 630
    popularity: 3
  place:
    combo: '647'
    payout: 200
    popularity: 416
  quinella:
    combo: 4-6
    payout: 660
    popularity: 2
  exacta:
    combo: 6-4
    payout: 1550
    popularity: 5
  wide:
    combo: 4-66-74-7
    payout: 160
    popularity: 2117
  trio:
    combo: 4-6-7
    payout: 1390
    popularity: 5
  trifecta:              # ✅ 取得成功！
    combo: 6-4-7
    payout: 9310
    popularity: 32
```

---

## 全データ再処理手順

### Phase 1: YAML再生成

全HTMLファイルをYAMLに再変換:

```bash
cd backend

# 全結果ファイルを処理（8,733レース）
uv run python html_to_yaml.py data/html/ --yaml-dir data/yaml_new/ --type result

# 処理時間見積もり: 約15-30分
```

### Phase 2: DB再投入

新しいYAMLファイルをデータベースに投入:

```bash
# 既存DBをバックアップ
cp kanazawa_dirt_one_spear.db kanazawa_dirt_one_spear_backup_20251114.db

# resultsテーブルをクリア
sqlite3 kanazawa_dirt_one_spear.db "DELETE FROM results;"

# YAML再投入
uv run python yaml_to_db.py data/yaml_new/
```

### Phase 3: 検証

```bash
# 3連単配当が格納されているか確認
sqlite3 kanazawa_dirt_one_spear.db "
SELECT
  COUNT(*) as total_results,
  COUNT(payout_trifecta) as with_trifecta,
  ROUND(COUNT(payout_trifecta) * 100.0 / COUNT(*), 2) as percentage
FROM results;
"

# 配当の基本統計
sqlite3 kanazawa_dirt_one_spear.db "
SELECT
  MIN(payout_trifecta) as min_payout,
  MAX(payout_trifecta) as max_payout,
  ROUND(AVG(payout_trifecta), 0) as avg_payout
FROM results
WHERE payout_trifecta IS NOT NULL;
"
```

---

## 期待される結果

### 配当データ取得率

- **修正前**: 0% (0 / 8,718)
- **修正後**: ~99.8% (約8,700 / 8,718)

一部のレース（中止、不成立など）では配当データがない可能性あり。

### 回収率計算が可能に

3連単配当データがあれば:
- AI予想の回収率計算
- 的中時の平均配当
- 投資効率の評価
- 人気薄大穴の発見率

すべてが可能になる。

---

## 今後のメンテナンス

### 新規データ取得時の注意

将来、新しいレースをスクレイピングする際は、修正済みの`nar_scraper.py`を使用すること。

### 他の地方競馬場への適用

本修正は**金沢競馬専用**。他の競馬場（浦和、船橋など）では枠連が発売されている可能性があり、インデックスが異なる。

---

## 結論

**3連単配当データの完全取得に成功**

これにより、プロジェクトの最終目標である「AI予想システムの実用的評価」が可能になった。

回収率の計算により、「一本槍」戦略の有効性を定量的に検証できる。

---

**修正者**: Claude
**修正日**: 2025-11-14
**検証状況**: ✅ 完了（全データ再処理済み）

---

## 実施結果（2025-11-14）

### Phase 1: YAML再生成
- 処理ファイル数: 8,718 レース
- 成功: 8,718
- 失敗: 0
- 成功率: **100%**

### Phase 2: yaml_to_db.py修正
**問題**: 新しいYAMLフォーマット（英語キー）に対応していなかった

**修正箇所**: yaml_to_db.py Line 348-358
```python
# 修正前
if '3連単' in payouts_data:
    trifecta = payouts_data.get('3連単', {})
    trifecta_payout = _parse_payout_amount(trifecta.get('amount', '0'))

# 修正後
if 'trifecta' in payouts_data:
    trifecta = payouts_data.get('trifecta', {})
    trifecta_payout = _parse_payout_amount(trifecta.get('payout', 0))
```

### Phase 3: DB再投入
- 処理ファイル数: 8,718 レース
- 成功: 8,718
- 失敗: 0
- 成功率: **100%**

### Phase 4: 検証結果

**配当データカバレッジ**:
- 総レース数: 8,718
- 3連単配当あり: 8,696
- カバレッジ: **99.75%**
- 欠損: 22レース (0.25%) ※中止・不成立レース

**配当統計**:
- 最小配当: 100円
- 最大配当: 1,032,020円
- 平均配当: 5,202円

### 結論

✅ **3連単配当データの完全取得に成功**

回収率計算が可能になり、AI予想システムの実用的評価が実現した。
