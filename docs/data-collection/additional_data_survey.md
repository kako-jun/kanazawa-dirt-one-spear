# 追加データ調査結果

**調査日**: 2025-11-15
**目的**: 既存HTMLからの追加データ抽出可能性と、追加スクレイピング必要性の調査

---

## 1. 既存HTMLに含まれているデータ

### レース結果 (race_XX_result.html)

**すでにYAMLに抽出済み:**
- ✅ 天候 (`weather: '曇'`)
- ✅ 馬場状態 (`track_condition: '良'`)
- ✅ 性齢 (`sex_age: '牡 3'`) - 馬齢データ
- ✅ 斤量 (`weight_carried: '56.0'`)
- ✅ 馬体重 (`horse_weight: '461'`)
- ✅ 馬体重増減 (`weight_diff: '0'`)
- ✅ 上り3F (`last_3f: '39.6'`)
- ✅ 上り4F (`last_4f: '52.0'`)
- ✅ コーナー通過順 (`corner_positions`)

**HTMLにあるがまだ抽出していないデータ:**
- ⚠️ **血統情報** (html:869-881行目)
  - 父馬、母馬、父の父、父の母、母の父、母の母
  - 例: `父: フサイチリシャール (父父: クロフネ、父母: フサイチエアデール)`
  - 取得元: レース結果HTMLの「馬情報」セクション

- ⚠️ **生年月日** (html:887行目)
  - 例: `2013年3月18日`
  - これで正確な馬齢を計算可能

- ⚠️ **生産牧場・産地** (html:889-895行目)
  - 例: `静内酒井牧場`, `北海道日高郡新ひだか町`

**DBスキーマ拡張が必要:**
```sql
-- horsesテーブルに追加
ALTER TABLE horses ADD COLUMN birth_date DATE;
ALTER TABLE horses ADD COLUMN sire_id VARCHAR;  -- 父馬ID
ALTER TABLE horses ADD COLUMN dam_id VARCHAR;   -- 母馬ID
ALTER TABLE horses ADD COLUMN sire_of_sire_id VARCHAR;  -- 父の父
ALTER TABLE horses ADD COLUMN dam_of_sire_id VARCHAR;   -- 父の母
ALTER TABLE horses ADD COLUMN sire_of_dam_id VARCHAR;   -- 母の父
ALTER TABLE horses ADD COLUMN dam_of_dam_id VARCHAR;    -- 母の母
ALTER TABLE horses ADD COLUMN farm VARCHAR;             -- 生産牧場
ALTER TABLE horses ADD COLUMN birthplace VARCHAR;       -- 産地
```

---

## 2. 既存参照データ

### コースレコード (course_records.html)

**所在地**: `backend/data/reference_data/html/course_records.html`
**取得元**: https://www.keiba.go.jp/guide/course_record/?course=kana
**取得日**: 2025-11-12

**含まれる情報:**
- ✅ 競馬場名: `金沢`
- ✅ コース方向: `右`（右回り）
- ✅ 距離一覧: 900m, 1300m, 1400m, 1500m, 1700m, 1900m, 2000m, 2100m, 2600m
- ✅ 各距離のコースレコードタイム
- ✅ レコード保持馬・騎手・達成日

**含まれていない情報:**
- ❌ 直線距離
- ❌ コーナー数
- ❌ コース形状（楕円、洋梨型など）
- ❌ 枠・馬番の有利不利情報

**活用方法:**
距離マスターとしてDB統合し、レースタイムとの差分を特徴量化できる。

---

### 騎手マスターデータ (jockeys_kanazawa.html) ⭐ 重要

**所在地**: `backend/data/reference_data/html/guide/jockeys_kanazawa.html`
**取得元**: https://www.keiba.go.jp/guide/jockey/?belong=kana
**取得日**: 2025-11-12

**含まれる情報:**
- ✅ ライセンス番号 (例: `031238`)
- ✅ 騎手名 (例: `甲賀 弘隆`)
- ✅ 読み仮名 (例: `こうが ひろたか`)
- ✅ **生年月日** (例: `19950821`) ⭐
- ✅ 性別 (`male`/`female`)
- ✅ 所属 (`kana` = 金沢)

**HTMLデータ構造:**
```html
<li class="guideList__item" data-belong="kana" data-sex="male" data-name="ko" data-birth="19950821">
  <a href="https://www.keiba.go.jp/KeibaWeb/DataRoom/RiderMark?k_riderLicenseNo=031238" ...>
    <p class="guideList__name">甲賀 弘隆</p>
    <p class="guideList__firigana">こうが ひろたか</p>
  </a>
</li>
```

**活用方法:**
- 騎手マスターテーブルとしてDB統合
- 生年月日から騎手の年齢を計算 → 年齢別成績分析が可能
- 読み仮名でフロントエンドでの検索性向上

**DBスキーマ拡張:**
```sql
-- jockeysテーブルに追加
ALTER TABLE jockeys ADD COLUMN birth_date DATE;
ALTER TABLE jockeys ADD COLUMN furigana VARCHAR;
ALTER TABLE jockeys ADD COLUMN gender VARCHAR;
```

---

## 3. 追加スクレイピングが必要なデータ

### 優先度: 高

#### (1) コース詳細情報

**必要な情報:**
- 直線距離 (例: 金沢は約XXXm)
- コーナー数 (例: 4コーナー)
- コース形状の特徴

**調査が必要:**
- 公式サイトに詳細情報ページがあるか確認
- 候補URL: https://www.keiba.go.jp/guide/course/ (コースガイドページ)
- なければ、最悪の場合は手動入力で済む（金沢のみで数は少ない）

#### (2) 血統データの正式取得

**現状:**
- レース結果HTMLに含まれているが未抽出
- パーサー拡張が必要

**対応:**
- `html_to_yaml.py`を拡張して血統セクションをパース
- horsesテーブルに血統カラムを追加

### 優先度: 中

#### (3) 馬の過去成績詳細

**候補URL:**
- 各馬の詳細ページ（レース結果HTMLからリンクあり）
- 例: `/KeibaWeb/DataRoom/HorseMarkInfo?k_lineageLoginCode=30036405106`

**懸念:**
- すでに `race_performances` テーブルに全レースデータがあるため、重複の可能性
- 必要性を検討してから取得を決定

#### (4) オッズ詳細データ

**現状:**
オッズページへのリンクはあるが未取得:
```html
<a href='/KeibaWeb/TodayRaceInfo/OddsTanFuku?k_raceDate=2016-10-25&k_raceNo=9&k_babaCode=22'>
オッズ
</a>
```

**方針:**
- ユーザーの方針: 「レース後のオッズで十分。購入締切直前にすればいい」
- → **レース確定後のオッズ（最終オッズ）のみ取得**
- → 時系列でのオッズ変動は不要

**取得戦略:**
1. レース結果ページから最終オッズへのリンクを辿る
2. 単勝・複勝・馬連・3連単などの最終オッズを取得
3. DBに `final_odds` テーブルを作成

---

## 4. 追加不要なデータ（レース結果から計算可能）

以下は `backend/data/reference_data/html/guide/` に保存済みだが、**使用しない**:

- ❌ 騎手リーディング (2022-2024)
- ❌ 調教師リーディング (2022-2024)
- ❌ 重賞優勝馬一覧

**理由:**
- 11年分のレース結果データから計算可能
- 統計テーブル (`stat_jockey_cumulative`, `stat_trainer_cumulative`) で代替

---

## 5. 実装計画

### Phase A: 既存データの完全活用（優先度: 最高）

1. **騎手マスターデータのパース実装** ⭐ 最優先
   - `jockeys_kanazawa.html`のパーサー実装
   - jockeysテーブルのスキーマ拡張（生年月日、読み仮名、性別）
   - DB統合スクリプト作成

2. **血統データのパース実装**
   - `html_to_yaml.py` の拡張（レース結果HTMLの馬情報セクション）
   - horsesテーブルのスキーマ拡張
   - 血統データのYAML/DB統合

3. **馬の生年月日の抽出**
   - レース結果HTMLから抽出
   - 正確な馬齢計算を可能にする

4. **コースレコードのDB統合**
   - `course_records` テーブル作成
   - 距離マスターとして活用

### Phase B: 追加スクレイピング（優先度: 高）

1. **コース詳細情報の調査**
   - https://www.keiba.go.jp/guide/course/ を確認
   - スクレイピング可能ならパーサー実装
   - 不可能なら手動入力（金沢のみ）

2. **最終オッズの取得**
   - オッズページのHTML構造調査
   - パーサー実装
   - DBスキーマ設計

### Phase C: 検討中（優先度: 低）

- 馬の詳細ページからの追加情報
- 他の参照データ

---

## 6. 次のアクション

1. ✅ 調査完了（本ドキュメント作成）
2. ⏳ 血統データパーサーの実装
3. ⏳ コース詳細情報の調査（公式サイト確認）
4. ⏳ 最終オッズ取得の設計

---

**最終更新**: 2025-11-15
**次のレビュー**: Phase A完了後
