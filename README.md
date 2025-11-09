# 金沢ダート一本槍 / Kanazawa Dirt One Spear

⚔️ 金沢競馬AI予想システム - 3連単一本勝負

## コンセプト

- **金沢競馬特化**: 地方競馬・金沢競馬を応援
- **一本槍予想**: 3連単を1点のみ予想（潔い！）
- **趣味・無料**: 営利目的ではなく、競馬ファンとして楽しむ
- **人柱記録**: 実際に購入した結果を記録・公開

## 技術スタック

### Frontend
- Next.js 14 (Static Export)
- React 18
- TypeScript 5
- Tailwind CSS 3

### Backend
- Python 3.11
- FastAPI
- SQLAlchemy + SQLite
- LightGBM (機械学習)

## 開発

### 1. Docker Composeで起動（推奨）

```bash
# すべてのサービスを起動
docker compose up --build

# バックグラウンドで起動
docker compose up -d

# サンプルデータを投入
docker compose exec backend python -m app.sample_data
```

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 2. ローカル開発

#### Backend

```bash
cd backend

# 依存関係インストール（uv使用）
pip install uv
uv pip install -r pyproject.toml

# サーバー起動
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# サンプルデータ投入
python -m app.sample_data
```

#### Frontend

```bash
cd frontend

# 依存関係インストール
npm install

# 開発サーバー起動
npm run dev
```

## 使い方

### 1. レース確認
- トップページでレース一覧を確認
- レースをクリックして詳細・予想を表示

### 2. 予想確認
- 「槍と団子」で3連単予想を視覚的に表示
- 馬番号・馬名・騎手名・信頼度を確認

### 3. 結果記録
- レース終了後、「結果を記録する」ボタンをクリック
- 着順・配当を入力
- 実際に購入した場合は購入フラグ + 金額を入力
- メモ・感想を記録（任意）

### 4. 統計確認
- 「📝 予想履歴」で過去の予想と結果を確認
- 「📊 的中実績」で的中率・回収率・収支を確認

## データ取得

### 自動データ収集（NAR公式サイトから）

```bash
# 未来のレース（今月・来月の出馬表）を取得
docker compose exec backend python -m app.fetch_races --future

# 過去のレース結果を取得
docker compose exec backend python -m app.fetch_races --past

# 特定日のレースを取得
docker compose exec backend python -m app.fetch_races --date 2025-01-15
```

**注意事項:**
- NAR公式サイト（keiba.go.jp）から取得
- リクエスト間隔3秒（サーバーに負荷をかけない）
- 1日1回の実行を推奨
- スクレイピングのため、サイト構造変更時は要修正

### 定期実行（cron設定例）

```bash
# 毎朝7時に未来のレースを取得
0 7 * * * cd /path/to/project && docker compose exec backend python -m app.fetch_races --future

# 毎晩21時に当日の結果を確認
0 21 * * * cd /path/to/project && docker compose exec backend python -m app.fetch_races --date $(date +%Y-%m-%d)
```

### データベース

- SQLite: `backend/kanazawa_dirt_one_spear.db`
- バックアップ: DBファイルをコピーするだけ

### 手動レース登録（管理API）

```bash
# APIでレースを登録
curl -X POST http://localhost:8000/api/admin/races \
  -H "Content-Type: application/json" \
  -d @race_data.json

# 予想を生成
curl -X POST http://localhost:8000/api/admin/predictions/{race_id}
```

## 今後の実装予定

- [ ] CSV/PDFパーサー（公式データ取り込み）
- [ ] LightGBM学習機能
- [ ] グラフ表示（的中率推移など）
- [ ] SNS共有機能
- [ ] 過去データ分析ツール

## 免責事項

※本サイトは趣味・無料・応援目的のAI予想サイトです
※予想は必ず当たるものではありません
※ギャンブルは適度に楽しみましょう

---

⚔️ 金沢競馬を一本槍で応援！
