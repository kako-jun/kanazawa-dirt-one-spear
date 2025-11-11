# ガイドページデータ (Guide Page Data)

このディレクトリには、金沢競馬ガイドページから取得した参照データを格納しています。

## 取得日

2025-11-12

## データ一覧

### 騎手関連

**jockeys_kanazawa.html** (201KB)
- URL: https://www.keiba.go.jp/guide/jockey/?belong=kana
- 内容: 金沢所属騎手一覧
- 情報: 騎手名、読み仮名、ライセンス番号

**rider_leading_2024.html** (26KB)
- URL: https://www.keiba.go.jp/KeibaWeb/DataRoom/RiderLeading?k_nenndo=2024&k_syozoku=6
- 内容: 2024年金沢騎手成績
- 情報: 順位、騎手名、1着～5着・着外数、合計、勝率、連対率、賞金

**rider_leading_2023.html** (27KB)
- 2023年金沢騎手成績

**rider_leading_2022.html** (24KB)
- 2022年金沢騎手成績

### 調教師関連

**trainer_leading_2024.html** (30KB)
- URL: https://www.keiba.go.jp/KeibaWeb/DataRoom/TrainerLeading?k_nenndo1=2024&k_syozoku=6
- 内容: 2024年金沢調教師成績
- 情報: 順位、調教師名、1着～5着・着外数、合計、勝率、連対率、賞金

**trainer_leading_2023.html** (27KB)
- 2023年金沢調教師成績

**trainer_leading_2022.html** (28KB)
- 2022年金沢調教師成績

### 重賞関連

**grade_race_winners.html** (229KB)
- URL: https://www.keiba.go.jp/KeibaWeb/DataRoom/JyusyoRaceWinhorse?k_babaCode=22
- 内容: 金沢競馬場の重賞優勝馬一覧（全年度）
- 情報: レース名、優勝馬名、騎手名、開催日

## データの用途

これらのデータは**レース情報との重複を確認するため**に取得しました。

### 予想への活用可能性

データ取得計画書(`backend/data_acquisition_plan.md`)に記載の通り:
- **騎手成績**: レース結果から計算可能（11年分のデータで十分）
- **調教師成績**: レース結果から計算可能
- **重賞優勝馬**: レース結果から抽出可能

### 結論

**これらのデータは使用しない**

理由:
1. レース情報（2015-2022年）に全て含まれている
2. 統計データは後から計算で生成できる
3. 重複データの保守コストが無駄

### 保存理由

- データ構造の確認用
- 将来的な検証用
- パーサー実装時の参照用

## 注意

このディレクトリのデータは**参照のみ**で、実際のパース・DB統合は行いません。
