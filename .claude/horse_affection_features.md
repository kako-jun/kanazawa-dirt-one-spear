# 愛着のわくコーナー - 機能仕様

## 概要

金沢競馬の馬や騎手への親しみを深め、データだけでなく「愛着」という観点からも楽しめるコンテンツを提供する。

## 機能一覧

### 1. かっこいい名前の馬ランキング

**目的**: 印象的な馬名を紹介し、馬への興味を引き出す

**実装内容**:
- 馬名の文字数、使用漢字、響きなどから「かっこいい度」を算出
- ユーザー投票機能（いいね！ボタン）
- カテゴリ別ランキング
  - 漢字がかっこいい
  - カタカナがかっこいい
  - 意味深い名前
  - 強そうな名前

**API設計**:
```
GET /api/horses/cool-names
Response: [
  {
    "horse_id": "...",
    "name": "サムライスピリット",
    "coolness_score": 95,
    "vote_count": 123,
    "category": "強そうな名前"
  }
]
```

### 2. 出走回数ランキング（常連馬）

**目的**: 金沢競馬を支える「常連馬」に光を当てる

**実装内容**:
- 通算出走回数トップ50
- 年度別出走回数ランキング
- 連続出走記録
- 馬齢別出走回数（若手/ベテラン）

**表示情報**:
- 馬名
- 出走回数
- 初出走日
- 最終出走日
- キャリア年数
- 代表的なレース名

**API設計**:
```
GET /api/horses/most-races?year=2024&limit=50
Response: [
  {
    "horse_id": "...",
    "name": "ゴールドラッシュ",
    "total_races": 87,
    "first_race_date": "2018-04-01",
    "last_race_date": "2024-11-10",
    "career_years": 6.5,
    "notable_races": ["金沢スプリント", "北國王冠"]
  }
]
```

### 3. 成績ランキング

**目的**: 優秀な成績を残した馬を称える

**実装内容**:
- **勝率ランキング**: 出走10回以上の馬を対象
- **連対率ランキング**: 1着・2着の割合
- **複勝率ランキング**: 1着・2着・3着の割合
- **年度別ランキング**
- **距離別ランキング**: 短距離/中距離/長距離

**最低出走回数のフィルタ**:
- デフォルト: 10回以上
- ユーザーが変更可能（5回、10回、20回、50回）

**表示情報**:
- 順位
- 馬名
- 出走回数
- 1着/2着/3着回数
- 勝率/連対率/複勝率
- 獲得賞金総額（データがあれば）

**API設計**:
```
GET /api/horses/win-rate?min_races=10&year=2024&limit=50
Response: [
  {
    "rank": 1,
    "horse_id": "...",
    "name": "スピードキング",
    "total_races": 45,
    "wins": 18,
    "places": 12,
    "shows": 8,
    "win_rate": 0.40,
    "place_rate": 0.67,
    "show_rate": 0.84,
    "total_prize": 12500000
  }
]
```

### 4. 年齢ランキング

**目的**: 最年長・最年少の馬を紹介し、馬の成長や引退のストーリーを感じさせる

**実装内容**:
- **最年長馬ランキング**: 現役最高齢
- **最年少馬ランキング**: デビューしたての若手
- **年齢別出走数分布**: 2歳〜10歳以上の出走傾向
- **ベテランの活躍**: 8歳以上で勝利した馬

**表示情報**:
- 馬名
- 年齢
- 出走回数
- 直近のレース結果
- デビュー年

**API設計**:
```
GET /api/horses/age-ranking?sort=desc&limit=20
Response: [
  {
    "horse_id": "...",
    "name": "レジェンドホース",
    "age": 11,
    "total_races": 102,
    "recent_result": "3着",
    "debut_year": 2015
  }
]
```

### 5. 騎手ランキング

**目的**: 騎手の活躍を可視化し、応援したくなる要素を提供

**実装内容**:
- **勝率ランキング**: 騎乗10回以上
- **騎乗回数ランキング**: 多く騎乗している騎手
- **年度別新人騎手成績**: デビュー騎手の活躍
- **騎手×馬のベストコンビ**: 相性の良い組み合わせ

**表示情報**:
- 騎手名
- 騎乗回数
- 勝利数
- 勝率
- 得意な馬場状態
- 得意な距離

**API設計**:
```
GET /api/jockeys/rankings?sort=win_rate&min_rides=10&year=2024
Response: [
  {
    "jockey_name": "山田太郎",
    "total_rides": 156,
    "wins": 42,
    "places": 38,
    "shows": 24,
    "win_rate": 0.27,
    "favorite_condition": "良",
    "favorite_distance": "1500m"
  }
]
```

### 6. 馬の詳細プロフィールページ

**目的**: 個々の馬のストーリーを深掘りする

**実装内容**:
- **基本情報**: 馬名、年齢、性別、毛色
- **過去戦績一覧**: 日付、レース名、着順、騎手、タイム
- **グラフ表示**: 成績推移、距離別成績
- **写真**: 馬の写真（データがあれば）
- **コメント欄**: ユーザーが応援メッセージを投稿（将来）
- **関連する馬**: 同じ厩舎、同じ血統（データがあれば）

**URL例**:
```
/horses/[horse_id]
```

### 7. お気に入り馬登録機能

**目的**: ユーザーが応援したい馬を登録し、パーソナライズされた体験を提供

**実装内容**:
- **お気に入り登録**: ハートマーク等で登録
- **マイページ**: お気に入り馬の一覧
- **通知**: お気に入り馬が出走する際の通知（将来）
- **応援メッセージ**: お気に入り馬に対するコメント

**データモデル**:
```python
class FavoriteHorse:
    user_id: str
    horse_id: str
    registered_at: datetime
    memo: str  # ユーザーの応援メモ
```

## データベース拡張

### 新しいテーブル

**horse_stats** (馬の統計情報キャッシュ):
```sql
CREATE TABLE horse_stats (
    horse_id VARCHAR PRIMARY KEY,
    total_races INTEGER,
    wins INTEGER,
    places INTEGER,
    shows INTEGER,
    win_rate FLOAT,
    place_rate FLOAT,
    show_rate FLOAT,
    coolness_score INTEGER,  -- かっこよさスコア
    vote_count INTEGER,      -- ユーザー投票数
    updated_at TIMESTAMP
);
```

**jockey_stats** (騎手の統計情報):
```sql
CREATE TABLE jockey_stats (
    jockey_name VARCHAR PRIMARY KEY,
    total_rides INTEGER,
    wins INTEGER,
    places INTEGER,
    shows INTEGER,
    win_rate FLOAT,
    favorite_condition VARCHAR,
    favorite_distance INTEGER,
    updated_at TIMESTAMP
);
```

**user_favorites** (お気に入り馬):
```sql
CREATE TABLE user_favorites (
    user_id VARCHAR,
    horse_id VARCHAR,
    registered_at TIMESTAMP,
    memo TEXT,
    PRIMARY KEY (user_id, horse_id)
);
```

## フロントエンド実装

### 新しいページ

1. `/horses` - 馬一覧・ランキング
2. `/horses/[horse_id]` - 馬の詳細プロフィール
3. `/jockeys` - 騎手ランキング
4. `/favorites` - お気に入り馬一覧（要ログイン）

### 新しいコンポーネント

- `HorseRanking.tsx` - ランキング表示
- `HorseProfile.tsx` - 馬のプロフィール詳細
- `JockeyRanking.tsx` - 騎手ランキング
- `FavoriteButton.tsx` - お気に入り登録ボタン
- `StatisticsChart.tsx` - 成績グラフ表示

## 統計データの更新方法

### バッチ処理

**cron/update_stats.py**:
```python
def update_horse_stats():
    """馬の統計情報を更新"""
    # 全馬の出走データを集計
    # horse_statsテーブルを更新
    pass

def update_jockey_stats():
    """騎手の統計情報を更新"""
    # 全騎手の騎乗データを集計
    # jockey_statsテーブルを更新
    pass
```

**実行頻度**:
- レース結果登録後、即時更新
- または1日1回の定期実行

## 技術的な考慮事項

### パフォーマンス

- 統計情報はキャッシュテーブルで事前計算
- ランキングページはページネーション実装
- 画像は遅延読み込み（Lazy Loading）

### セキュリティ

- お気に入り機能は認証必須
- ユーザー投票は1日1回まで（スパム防止）

### UX

- ランキングはアニメーション付きで表示
- 馬名クリックで詳細ページへスムーズ遷移
- モバイルでも見やすいレスポンシブデザイン

## 実装優先順位

1. **フェーズ1** (即時実装可能):
   - 出走回数ランキング
   - 年齢ランキング
   - 馬の詳細プロフィールページ

2. **フェーズ2** (データ整備後):
   - 成績ランキング（勝率・連対率）
   - 騎手ランキング

3. **フェーズ3** (認証機能実装後):
   - お気に入り馬登録
   - かっこいい名前ランキング（投票機能）

## 参考デザイン

- netkeiba.com: 馬の詳細ページ
- JRA公式: ランキング表示
- Spotify: お気に入り機能のUX
