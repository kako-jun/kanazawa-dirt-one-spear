# CLAUDE.md - 開発者向けドキュメント

このドキュメントは、AIアシスタント（Claude）や開発者が本プロジェクトを理解・拡張するためのものです。

## プロジェクト概要

**金沢ダート一本槍（Kanazawa Dirt One Spear）**は、金沢競馬に特化したAI予想システムです。

### 特徴
- 3連単を1点のみ予想（一本槍スタイル）
- 実購入結果の記録・統計表示
- 趣味・無料・応援目的（非営利）

### プロジェクトの使命
**金沢競馬場の存続を支援する**
- 馬券購入を促進し、売上に貢献
- 馬や騎手、競馬場への愛着を育む
- 「応援」としての馬券購入文化を醸成

## アーキテクチャ

### フロントエンド (Next.js)

```
frontend/
├── src/
│   ├── app/
│   │   ├── globals.css           # グローバルスタイル
│   │   ├── layout.tsx            # ルートレイアウト
│   │   └── page.tsx              # メインページ（レース一覧/統計/履歴）
│   ├── components/
│   │   ├── RaceList.tsx          # レース一覧表示
│   │   ├── RaceDetail.tsx        # レース詳細・出馬表
│   │   ├── SpearPrediction.tsx   # 予想表示（槍と団子）
│   │   ├── ResultForm.tsx        # 結果入力フォーム
│   │   └── ResultHistory.tsx     # 予想履歴表示
│   └── lib/
│       └── api-client.ts         # バックエンドAPIクライアント
```

**主要コンポーネント**:
- `SpearPrediction`: 槍（穂先→団子3つ→柄）のビジュアル表示
- `ResultForm`: 着順・配当・購入情報の入力
- `ResultHistory`: 過去の予想結果を時系列表示

### バックエンド (FastAPI)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPIアプリ・エンドポイント定義
│   ├── models.py             # Pydanticモデル（API用）
│   ├── database.py           # SQLAlchemy設定・DBモデル
│   ├── crud.py               # CRUD操作
│   ├── predictor.py          # 予想ロジック
│   ├── sample_data.py        # サンプルデータ生成
│   └── scrapers/             # データ取得（将来実装）
│       └── __init__.py
└── pyproject.toml            # 依存関係定義
```

**データフロー**:
1. レースデータをDBに登録
2. `predictor.py`で予想生成（現在はシンプルルール、将来LightGBM）
3. フロントエンドで予想表示
4. ユーザーが結果を記録
5. 統計を自動計算

## データモデル

### データベーステーブル

**horses** (馬マスタ)
- horse_id (PK)
- name, age, gender

**races** (レース)
- race_id (PK)
- date, race_number, name
- distance, track_condition, weather

**entries** (出走情報)
- entry_id (PK)
- race_id (FK), horse_id (FK)
- gate_number, horse_number
- jockey, weight, odds
- past_results (JSON)

**predictions** (予想)
- prediction_id (PK)
- race_id (FK, unique)
- first, second, third
- confidence, model_version
- predicted_at

**results** (結果)
- result_id (PK)
- race_id (FK, unique)
- first, second, third
- payout_trifecta
- prediction_hit (bool)
- purchased (bool)
- bet_amount, return_amount
- recorded_at, memo

## API エンドポイント

### 公開API

**レース関連**
- `GET /api/races` - レース一覧（日付フィルター可）
- `GET /api/races/{race_id}` - レース詳細
- `GET /api/predictions/{race_id}` - 予想取得

**結果関連**
- `GET /api/results` - 結果一覧
- `POST /api/results` - 結果投稿
- `GET /api/stats` - 統計情報

### 管理API

- `POST /api/admin/races` - レース登録
- `POST /api/admin/predictions/{race_id}` - 予想生成

## 予想ロジック

### 現在の実装 (predictor.py)

シンプルなルールベース:
1. オッズが低い（人気）順に3頭選択
2. 信頼度は50-80%でランダム

### 将来の実装予定

**LightGBM Ranker**を使用:
- 特徴量: 枠番、騎手、斤量、馬齢、過去成績、馬場状態、オッズ
- 学習データ: 過去の金沢競馬データ
- 評価指標: NDCG、的中率、回収率

## 開発ガイドライン

### 新機能追加の流れ

1. **バックエンド**: データモデル → CRUD → API → 予想ロジック
2. **フロントエンド**: API型定義 → コンポーネント → ページ統合
3. **テスト**: サンプルデータで動作確認

### コーディング規約

**TypeScript**:
- 関数コンポーネントを使用
- `use client`ディレクティブ（Client Component）
- Tailwind CSSでスタイリング

**Python**:
- 型ヒント必須
- Pydanticでバリデーション
- SQLAlchemy ORMでDB操作

### データベースマイグレーション

現在は`init_db()`で自動生成。本番運用では Alembic を検討。

## トラブルシューティング

### データベースリセット

```bash
# DBファイル削除
rm backend/kanazawa_dirt_one_spear.db

# サーバー再起動で自動再作成
# サンプルデータ投入
python -m app.sample_data
```

### CORSエラー

`backend/app/main.py`で`allow_origins=["*"]`設定済み。
本番環境では適切なオリジンに制限すること。

## 今後の拡張

### 優先度高
1. **CSVパーサー**: NAR公式データを取り込み
2. **LightGBM実装**: 機械学習モデルでの予想
3. **データバックアップ**: 定期的なDB保存

### 優先度中
4. **グラフ表示**: Chart.jsで的中率推移
5. **SNS共有**: Twitter/noteへの投稿機能
6. **認証機能**: 複数ユーザー対応（必要なら）
7. **馬券購入促進機能**: 金沢競馬を応援する仕組み
   - 「楽天競馬で買う」ボタンの最適配置
   - 今週のイチオシレース・馬の紹介
   - 「100円から応援」少額購入の訴求
   - みんなの購入状況表示（ソーシャルプルーフ）
   - 当たった人の声・実績紹介
   - ゲーミフィケーション（バッジ、ランキング）
   - 「金沢競馬を守る」意識の醸成
   - 初心者向け購入ガイド
   - メール・プッシュ通知
8. **愛着のわくコーナー**: 馬や競馬への親しみを深める機能
   - かっこいい名前の馬ランキング
   - 出走回数ランキング（常連馬）
   - 成績ランキング（勝率・連対率・複勝率）
   - 年齢ランキング（最年長・最年少）
   - 騎手ランキング（勝率・騎乗回数）
   - 馬の詳細プロフィールページ（過去戦績、写真など）
   - お気に入り馬登録機能
9. **競馬場統計**: 金沢競馬場という「場所」に着目した統計
   - 年間レース数の推移（2015年〜現在）
   - 月別・曜日別の開催傾向
   - 距離別レース数の分布
   - 馬場状態・天候の統計
   - 出走頭数の統計
   - レース名の種類と傾向
   - 歴史的トピックス
   - 「そういえば知らなかった」を引き出す発見型コンテンツ

### 優先度低
10. **PDF解析**: 出馬表PDFの自動読み取り
11. **リアルタイムオッズ**: API連携（公式許可が必要）
12. **モバイルアプリ**: React Native

## 参考資料

- FastAPI: https://fastapi.tiangolo.com/
- Next.js: https://nextjs.org/docs
- SQLAlchemy: https://docs.sqlalchemy.org/
- LightGBM: https://lightgbm.readthedocs.io/

## ライセンス・法的配慮

- 趣味・非営利プロジェクト
- 公式データの利用規約遵守
- ギャンブル依存防止の注意書き表示
- 「必ず当たる」等の誤認表現禁止
