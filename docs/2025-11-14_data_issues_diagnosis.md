# データ異常の診断結果 - 2025-11-14

## 🔍 調査対象

EDAで発見された以下のデータ異常：
1. **馬場状態**: 「不良」が94.57%（明らかに異常）
2. **性別**: 50%が`None`、50%が`female`

---

## 📋 調査結果

### 問題1: 馬場状態データの異常

#### 現状
```
不良: 8,259レース（94.57%）
重: 474レース（5.43%）
良・稍重: 0レース
```

#### 原因特定

**ステップ1: YAMLファイルの確認**
- `data/yaml/YYYY/YYYYMMDD/race_NN_result.yaml` を確認
- ❌ `track_condition` フィールドが**存在しない**
- YAMLには馬場状態の情報が含まれていない

**ステップ2: html_to_yaml.pyの確認**
- `_parse_deba()`関数（89-100行目）: 出馬表HTMLから馬場状態を抽出 ✅
- `_parse_result()`関数（479行目〜）: 結果HTMLから馬場状態を抽出 ❌ **未実装**

**ステップ3: yaml_to_db.pyの確認**
- `import_result_yaml()`関数（306行目）:
  ```python
  track_condition=race_data.get('track_condition', '不明'),
  ```
  デフォルト値が「不明」

**結論**:
1. 結果HTMLには馬場状態の情報があるはず（通常のレース結果ページには記載されている）
2. `html_to_yaml.py`の`_parse_result()`がこれを抽出していない
3. YAMLファイルに`track_condition`フィールドがない
4. DBには「不明」が設定されている
5. データベース上で「不明」が「不良」として表示されている（理由不明、要確認）

---

### 問題2: 性別データの欠損

#### 現状
```
性別がfemale: 3,301頭（50.01%）
性別がNone: 3,300頭（49.99%）
```

#### 原因特定

**ステップ1: YAMLファイルの確認**
- result.yamlの`result_details`に`sex_age`フィールドあり ✅
- 例: `sex_age: 牝 4`, `sex_age: 牡 5`, `sex_age: セン 4`
- YAMLには正しいデータが含まれている

**ステップ2: yaml_to_db.pyの確認**
- `import_deba_yaml()`関数（186-220行目）:
  ```python
  sex_age = horse_data.get('sex_age', None)
  age, gender = _parse_sex_age(sex_age)
  horse.age = age
  horse.gender = gender
  ```
  ✅ 正しく処理している

- `import_result_yaml()`関数（266行目〜）:
  - `result_details`内の馬情報を**一切処理していない** ❌
  - 着順、配当、コーナー通過順のみを処理
  - 馬の詳細情報（性別、年齢、馬体重など）を無視

**ステップ3: _parse_sex_age()の確認**
- `_parse_sex_age()`関数（398-417行目）:
  ```python
  if '牡' in sex_age_str:
      gender = 'male'
  elif '牝' in sex_age_str:
      gender = 'female'
  elif 'セ' in sex_age_str:
      gender = 'gelding'
  ```
  ✅ パースロジックは正しい

**結論**:
1. YAMLファイルには性別情報が含まれている
2. `yaml_to_db.py`の`import_result_yaml()`が`result_details`を処理していない
3. `import_deba_yaml()`（出馬表）を使った場合のみ性別が登録される
4. 現在のDBには出馬表データがないため、result.yamlの情報のみが入っている
5. result.yamlの馬情報が処理されていないため、性別が登録されていない
6. DBに50%だけ性別が入っているのは、別の処理または以前のデータの残存の可能性

---

## 🎯 修正方針

### 方針A: html_to_yaml.pyを修正（根本解決）

**修正内容**:
1. `_parse_result()`関数に馬場状態・天候の抽出処理を追加
   - `_parse_deba()`と同様のロジックを実装（89-100行目を参考）
   - 結果HTMLの全テキストから正規表現で抽出
   - YAMLに`track_condition`と`weather`フィールドを追加

**メリット**:
- YAMLファイル自体が完全なデータを持つ
- 将来的な再利用が容易

**デメリット**:
- HTMLの再パース・YAML再生成が必要
- 処理時間がかかる

---

### 方針B: yaml_to_db.pyを修正（迅速対応）

**修正内容**:
1. `import_result_yaml()`関数を拡張
   - `result_details`内の馬情報を処理
   - 各馬の`sex_age`から性別・年齢を抽出
   - 馬マスタを更新

**メリット**:
- 既存YAMLファイルをそのまま使用可能
- 性別データの問題は即座に解決

**デメリット**:
- 馬場状態の問題は未解決（YAMLにデータがないため）

---

### 推奨: 方針A + 方針B の組み合わせ

**ステップ1: yaml_to_db.pyを先に修正**
- `import_result_yaml()`に`result_details`処理を追加
- DBを再投入して性別データを復元
- **即座に性別問題を解決**

**ステップ2: html_to_yaml.pyを修正**
- `_parse_result()`に馬場状態・天候抽出を追加
- 全HTMLを再パースしてYAML再生成
- **馬場状態問題を解決**

**ステップ3: 最終DB再投入**
- 完全なYAMLからDBを再構築
- データ検証

---

## 📝 実装詳細

### 修正1: yaml_to_db.py の import_result_yaml()

**追加箇所**: 386行目以降（result登録後）

```python
# result_details内の馬情報を処理
result_details_data = data.get('result_details', [])
for detail in result_details_data:
    horse_name = detail.get('horse_name', None)
    sex_age = detail.get('sex_age', None)

    if not horse_name or not sex_age:
        continue

    age, gender = _parse_sex_age(sex_age)

    # 馬マスタを検索（名前で検索、厳密にはhorse_idが必要だが名前で近似）
    horse = session.query(DBHorse).filter_by(name=horse_name).first()
    if horse and (not horse.age or not horse.gender):
        # 年齢・性別が未設定の場合のみ更新
        if age and not horse.age:
            horse.age = age
        if gender and not horse.gender:
            horse.gender = gender
```

**課題**:
- 馬名で検索しているため、同姓同名の馬がいる場合は誤動作
- 本来は`race_id`と`horse_number`から`entry`を特定し、そこから`horse_id`を取得すべき

---

### 修正2: html_to_yaml.py の _parse_result()

**追加箇所**: 565行目（last_4f抽出後）

```python
# 馬場状態を抽出
track_condition = "不明"
for cond in ["不良", "重", "稍重", "良"]:
    if cond in info_text:
        track_condition = cond
        break

# 天候を抽出
weather = "不明"
for w in ["雪", "雨", "曇", "晴"]:
    if w in info_text:
        weather = w
        break
```

**戻り値に追加**:
```python
return {
    'meta': { ... },
    'race_id': race_id,
    'track_condition': track_condition,  # 追加
    'weather': weather,                  # 追加
    'finish_order': finish_order,
    ...
}
```

---

## ⚠️ その他の確認事項

### 「不明」が「不良」として表示される問題

**可能性**:
1. データベース上で「不明」が「不良」として保存されている
2. 表示ロジックで「不明」→「不良」のマッピングが行われている
3. 文字コードの問題

**確認方法**:
```sql
SELECT track_condition, COUNT(*)
FROM races
GROUP BY track_condition;
```

実際のデータベース内の値を確認する必要がある。

---

## 📊 修正後の期待結果

### 性別データ
```
修正前:
  female: 3,301頭（50.01%）
  None: 3,300頭（49.99%）

修正後:
  female: ~3,300頭（50%）
  male: ~2,500頭（38%）
  gelding: ~800頭（12%）
  None: 0頭
```

### 馬場状態
```
修正前:
  不良: 94.57%
  重: 5.43%

修正後:
  良: ~60-70%
  稍重: ~15-20%
  重: ~10-15%
  不良: ~5%
```

---

## 🚀 次のアクション

### 優先度A（即実施）
1. データベースのtrack_condition値を直接確認
2. yaml_to_db.pyの修正（result_details処理）
3. DBテスト投入で検証

### 優先度B（並行実施）
4. html_to_yaml.pyの修正（馬場状態抽出）
5. 一部HTMLで動作検証

### 優先度C（最終実施）
6. 全YAML再生成
7. DB完全再投入
8. データ検証

---

**作成者**: Claude
**作成日**: 2025-11-14
**関連ファイル**:
- `backend/html_to_yaml.py`
- `backend/yaml_to_db.py`
- `backend/data/yaml/**/*.yaml`
