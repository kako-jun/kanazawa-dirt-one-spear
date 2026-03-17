# 使い方

## 全体の流れ

```
データ収集 → DB投入 → 統計構築 → モデル訓練 → 予想生成 → 結果記録
```

通常の週次運用は「データ収集」と「予想確認・結果記録」だけ行えばよい。モデルの再訓練は特徴量や統計テーブルを変更したときにのみ行う。

## 起動

Docker Composeを使うのが最も手軽：

```bash
docker compose up -d
```

- フロントエンド：http://localhost:3000
- バックエンドAPI：http://localhost:8000
- APIドキュメント：http://localhost:8000/docs

## ステップ1：データ収集

レース前（当日〜数日前）に出走表を取得する：

```bash
# 今月・来月の出走表を取得
docker compose exec backend python -m app.fetch_races --future

# 当日のレース情報を確認
docker compose exec backend python -m app.fetch_races --date 2025-06-15
```

レース後に結果を取得する：

```bash
# 当日の結果を取得
docker compose exec backend python -m app.fetch_races --past
```

リクエスト間隔は3秒に設定されている。1日1回の実行で十分。

### cron設定（自動化する場合）

```bash
# 毎朝7時に出走表を取得
0 7 * * * cd /path/to/project && docker compose exec backend python -m app.fetch_races --future

# 毎晩21時に当日結果を取得
0 21 * * * cd /path/to/project && docker compose exec backend python -m app.fetch_races --date $(date +%Y-%m-%d)
```

## ステップ2：統計テーブルの再構築（必要時のみ）

新しいレースデータをDBに追加した後、統計テーブルを最新の状態にする：

```bash
cd backend
uv run python build_stats_tables.py
```

1〜2分で完了する。統計の計算式を変更した場合も同様に再構築する。

## ステップ3：予想の確認

ブラウザでフロントエンドを開き、本日のレースを選択する。予想は自動的に表示される：

- 1着・2着・3着の予想馬番
- 各馬を選んだ理由（統計上の根拠）
- 信頼度スコア

信頼度が低い場合は購入を見送るのも一つの判断。100円を賭けるかどうか、最終的な判断は自分で行う。

## ステップ4：馬券の購入（任意）

予想を確認したら、NAR公式のネット投票サービス（SPAT4等）で実際に馬券を購入する。本システムは購入を自動化しない。購入するかどうか、何円賭けるかは手動で判断する。

推奨額：1レース100円（試行を多く積み重ねるため）

## ステップ5：結果の記録

レース終了後、フロントエンドの「結果を記録する」ボタンから入力する：

- 実際の着順（1〜3着の馬番）
- 3連単の払い戻し配当
- 購入フラグ（実際に買ったかどうか）
- 購入金額
- メモ・感想（任意）

予想が外れた場合も必ず記録する。外れのデータも改善に使える。

## ステップ6：統計の確認

「予想履歴」では過去の予想と結果の一覧が確認できる。「的中実績」では期間別の的中率・回収率・収支が集計されている。

長期的に回収率が100%を超えるかどうかが最終的な評価基準。単発で当たっても負けても、傾向が見えるのは数十〜数百回の記録が積み重なってから。

## モデルの再訓練（特徴量や統計を変えたとき）

```bash
cd analysis

# 特徴量CSVを再生成
uv run python feature_engineering_v2.py

# モデルを再訓練
uv run python train_lightgbm.py
```

訓練済みモデルはGitでバージョン管理する。性能比較レポートも同時に生成される。

## データのバックアップ

データベースファイルは `backend/data/kanazawa_dirt_one_spear.db` に保存されている。定期的にコピーしておくとよい。YAMLファイル（`backend/data/yaml/`）も同様に保管しておけば、DBを壊してもゼロから再構築できる。
