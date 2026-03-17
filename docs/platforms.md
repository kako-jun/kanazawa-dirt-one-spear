# 動作環境

## ブラウザ（フロントエンド）

モダンブラウザで動作する。特別なインストールは不要。

- Chrome / Edge / Firefox（最新版）
- モバイルブラウザでも基本的に動作する

フロントエンドはNext.jsで構築されており、バックエンドAPIと通信して表示する。静的エクスポートにも対応しているため、将来的にはAPIなしの静的サイトとして公開することも可能。

## Docker環境（推奨）

最も手軽に全体を動かす方法。フロントエンド・バックエンド・依存関係がすべてコンテナ内に収まる。

必要なもの：
- Docker Desktop（Mac / Windows / Linux）
- Docker Compose v2以上

起動コマンド：
```bash
docker compose up -d
```

各コンテナの役割：
- `frontend`：Next.js開発サーバー（ポート3000）
- `backend`：FastAPIサーバー（ポート8000）

コンテナを使わずにローカル開発する場合は、フロントエンドとバックエンドをそれぞれ別ターミナルで起動する。

## Python / FastAPI（バックエンド）

バックエンドはPythonで書かれており、以下のスタックを使用している。

- **Python 3.11**
- **FastAPI**：REST APIフレームワーク。自動生成のAPIドキュメント（Swagger UI）が `localhost:8000/docs` で確認できる
- **SQLAlchemy**：ORMおよびSQLビルダー
- **Pydantic**：データバリデーション
- **uvicorn**：ASGIサーバー

依存関係の管理には `uv` を使用している。Python実行は `uv run python3` で行う。

分析・機械学習系の追加ライブラリ：
- **LightGBM**：勾配ブースティング。予測モデルの本体
- **pandas / numpy**：データ処理
- **scikit-learn**：前処理・評価指標
- **SHAP**：モデルの予測根拠を可視化（将来実装）
- **Optuna**：ハイパーパラメータ最適化（将来実装）

## SQLite（開発・単体運用）

デフォルトのデータベースはSQLite。ファイル1つで動作し、インストール不要。

- ファイルパス：`backend/data/kanazawa_dirt_one_spear.db`
- バックアップはファイルをコピーするだけ
- 開発中の試行錯誤に向いている

テーブル構造：
- 生データ層（races, horses, jockeys, trainers, entries, race_performances, payouts）
- 統計層（stat_* プレフィクスのテーブル群）

## PostgreSQL（スケールアップ時）

将来的に複数ユーザーへの公開やデータ量増加に対応する場合、PostgreSQLへの移行を想定している。SQLAlchemyを使っているため、接続先URLを変更するだけで移行できる設計になっている。

現状ではSQLiteで十分。

## フロントエンド技術スタック

- **Next.js 14**（App Router）：React製のフレームワーク
- **React 18**
- **TypeScript 5**：型安全な実装
- **Tailwind CSS 3**：スタイリング
- **静的エクスポート対応**：将来の公開に向けて

## 開発ツール

- **uv**：Pythonパッケージ管理（pipより高速）
- **npm**：フロントエンドパッケージ管理
- **SQLite CLI**：データベースの直接確認
- **curl / httpie**：APIのテスト
