# 参照データ (Reference Data)

このディレクトリには、レース情報とは独立した恒久的な参照データを格納しています。

## ディレクトリ構造

```
reference_data/
├── html/                  # 元のHTMLファイル
│   └── course_records.html
├── json/                  # パース済みJSONファイル
│   └── course_records.json
└── README.md
```

## データソース

### コースレコード (course_records.json)

**取得元**: https://www.keiba.go.jp/guide/course_record/?course=kana

**取得日**: 2025-11-12

**内容**: 金沢競馬場の距離別コースレコード

**データ構造**:
```json
{
  "course": "金沢",
  "direction": "右回り",
  "records": [
    {
      "distance": 900,
      "record_time": "0:53.6",
      "record_seconds": 53.6,
      "horse_name": "ニュータウンガール",
      "jockey_name": "岡部　誠",
      "achieved_date": "2021-06-29"
    },
    ...
  ]
}
```

**距離一覧**:
- 900m: 0:53.6
- 1300m: 1:21.9
- 1400m: 1:24.6
- 1500m: 1:32.1
- 1700m: 1:45.9
- 1900m: 1:59.8
- 2000m: 2:04.9
- 2100m: 2:10.3
- 2600m: 2:49.5

**用途**:
- 距離別の基準タイムとして予想モデルに活用
- レースタイムとの差分を特徴量化
- 距離マスタとしてDB統合

## 更新方法

### コースレコードの更新

1. HTMLを再取得:
```bash
curl -s "https://www.keiba.go.jp/guide/course_record/?course=kana" -o data/reference_data/html/course_records.html
```

2. パース実行:
```bash
uv run python parse_course_records.py
```

3. JSONファイルを確認:
```bash
cat data/reference_data/json/course_records.json
```

## 更新頻度

コースレコードは年に数回程度の更新のため、**年1回程度の再取得**で十分です。

## データベース統合

`course_records.json` は以下のテーブルに統合される予定:

**course_records** テーブル:
- distance (PK)
- record_time
- record_seconds
- horse_name
- jockey_name
- achieved_date

統合スクリプト: `(未実装)`
