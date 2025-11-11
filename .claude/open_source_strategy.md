# オープンソース化戦略 - 地方競馬を全国で盛り上げる

## ビジョン

**「金沢競馬で成功したノウハウを他の地方競馬場でも活用できるようにする」**

このプロジェクトをオープンソース化し、全国15の地方競馬場でそれぞれのファンがサイトを立ち上げられるようにする。
地方競馬全体の活性化に貢献し、廃止の危機を回避する。

## 対象となる地方競馬場（NAR加盟15場）

1. **帯広競馬場**（ばんえい競馬）- 北海道
2. **門別競馬場** - 北海道
3. **盛岡競馬場** - 岩手県
4. **水沢競馬場** - 岩手県
5. **浦和競馬場** - 埼玉県
6. **船橋競馬場** - 千葉県
7. **大井競馬場** - 東京都
8. **川崎競馬場** - 神奈川県
9. **金沢競馬場** - 石川県（本プロジェクト）
10. **笠松競馬場** - 岐阜県
11. **名古屋競馬場** - 愛知県
12. **園田競馬場** - 兵庫県
13. **姫路競馬場** - 兵庫県
14. **高知競馬場** - 高知県
15. **佐賀競馬場** - 佐賀県

## オープンソース化の方針

### ライセンス

**MIT License** を推奨:
- 商用利用可
- 改変・再配布可
- ライセンス表示のみ義務
- 他競馬場が自由にカスタマイズできる

### リポジトリ構成

**メインリポジトリ**:
```
kanazawa-dirt-one-spear/
├── README.md                    # プロジェクト概要
├── docs/
│   ├── getting-started.md       # はじめ方ガイド
│   ├── how-to-customize.md      # カスタマイズ方法
│   ├── deployment.md            # デプロイ手順
│   └── architecture.md          # アーキテクチャ解説
├── backend/                     # バックエンドコード
├── frontend/                    # フロントエンドコード
└── examples/
    └── config.sample.yaml       # 設定ファイルサンプル
```

### 汎用化のための設計変更

**設定ファイルで競馬場を切り替え**:

`config.yaml`:
```yaml
racecourse:
  name: "金沢競馬場"
  short_name: "金沢"
  nar_code: "kanazawa"
  region: "石川県"
  website: "https://www.kanazawa-racing.jp/"

scraping:
  base_url: "https://www.nar.or.jp/"
  racecourse_id: "kanazawa"

branding:
  site_title: "金沢ダート一本槍"
  primary_color: "#1E40AF"  # 金沢のテーマカラー
  logo_path: "/assets/logo-kanazawa.png"

features:
  enable_betting_promotion: true
  enable_affection_corner: true
  enable_statistics: true
```

**他競馬場用のサンプル設定**:

`examples/config-ooi.yaml` (大井競馬):
```yaml
racecourse:
  name: "大井競馬場"
  short_name: "大井"
  nar_code: "ooi"
  region: "東京都"

branding:
  site_title: "大井競馬ファンサイト"
  primary_color: "#DC2626"  # 大井のテーマカラー
```

### 汎用スクレイパーの実装

**競馬場IDを渡すだけで動作**:

`backend/app/scrapers/universal_nar_scraper.py`:
```python
class UniversalNARScraper:
    """全国の地方競馬場に対応したスクレイパー"""

    def __init__(self, racecourse_code: str):
        self.racecourse_code = racecourse_code  # 'kanazawa', 'ooi', etc.
        self.config = load_config(racecourse_code)

    def scrape_schedule(self, year: int):
        """指定競馬場のスケジュールを取得"""
        url = f"{self.config['base_url']}/schedule/{self.racecourse_code}/{year}"
        # NAR公式のURLパターンに合わせて取得
        pass
```

## ドキュメント整備

### 1. 導入ガイド（Getting Started）

**対象**: 他競馬場でサイトを作りたい人

**内容**:
```markdown
# 〇〇競馬場版の作り方

## ステップ1: リポジトリをフォーク
git clone https://github.com/your-name/kanazawa-dirt-one-spear.git
cd kanazawa-dirt-one-spear

## ステップ2: 設定ファイルをコピー
cp examples/config-sample.yaml config.yaml

## ステップ3: 競馬場情報を編集
# config.yamlを開いて、あなたの競馬場の情報に書き換え

## ステップ4: データ取得
uv run python scrape_schedule.py --racecourse ooi --year 2024

## ステップ5: サーバー起動
cd backend && uv run python -m app.main
cd frontend && npm run dev

## ステップ6: カスタマイズ
- ロゴを差し替え
- テーマカラーを変更
- 独自機能を追加
```

### 2. カスタマイズガイド

**カスタマイズ可能な箇所**:
- サイト名・タイトル
- テーマカラー
- ロゴ・ファビコン
- トップページの文言
- 独自の統計機能追加
- ローカルイベント情報

**例: 大井競馬用にカスタマイズ**:
```typescript
// frontend/src/config.ts
export const SITE_CONFIG = {
  name: "大井競馬ファンサイト",
  description: "トゥインクルレースを盛り上げる",
  racecourse: "大井",
  themeColor: "#DC2626",
  specialFeatures: [
    "トゥインクルレース特集",
    "東京シティ競馬ナイター分析"
  ]
}
```

### 3. デプロイ手順

**無料で始められるホスティング**:

- **フロントエンド**: Vercel / Netlify（無料枠）
- **バックエンド**: Fly.io / Railway（無料枠）
- **データベース**: SQLite（ファイルベース） or Supabase（無料枠）

**ドキュメント例**:
```markdown
# Vercelへのデプロイ

1. Vercelアカウント作成（無料）
2. GitHubリポジトリと連携
3. 環境変数を設定:
   - RACECOURSE_CODE=ooi
   - API_URL=https://your-backend.fly.dev
4. デプロイボタンを押すだけ
```

### 4. アーキテクチャドキュメント

**システム構成の説明**:
- なぜNext.jsを選んだか
- なぜFastAPIを選んだか
- データベース設計の考え方
- スクレイピングの仕組み
- 予想エンジンの仕組み

### 5. トラブルシューティング

**よくある問題と解決方法**:
- スクレイピングが動かない
- データが表示されない
- デプロイに失敗する
- カスタマイズ方法がわからない

## コミュニティ構築

### Discordサーバー

**「地方競馬ファンサイト開発者コミュニティ」**:
- チャンネル構成:
  - `#general` - 雑談
  - `#金沢` - 金沢競馬版
  - `#大井` - 大井競馬版
  - `#その他の競馬場` - 他競馬場
  - `#tech-support` - 技術サポート
  - `#feature-ideas` - 機能アイデア
  - `#showcase` - 完成したサイトの紹介

### GitHub Discussions

**質問・提案の場**:
- Q&A: 技術的な質問
- Ideas: 新機能の提案
- Show and tell: 「〇〇競馬版作りました！」

### 月次オンラインミーティング

**開発者同士の交流**:
- 各競馬場の進捗共有
- ベストプラクティスの共有
- 困っていることの相談

## 技術サポート体制

### ドキュメント

- **Wiki**: よくある質問と回答
- **API仕様書**: 自動生成（FastAPIのSwagger）
- **動画チュートリアル**: YouTube（将来的に）

### サンプルコード集

**examples/**:
```
examples/
├── custom-statistics/       # 独自統計の追加例
├── custom-theme/           # テーマカスタマイズ例
├── local-events/           # ローカルイベント機能
└── multilingual/           # 多言語対応例（帯広=英語も？）
```

### Issue Templates

**GitHub Issueテンプレート**:
- Bug Report（バグ報告）
- Feature Request（機能要望）
- Help Wanted（助けてほしい）
- My Racecourse（〇〇競馬版を作っています報告）

## 貢献者募集

### 求めるスキル

**初心者でもOK**:
- 各競馬場のローカル知識
- デザインセンス（UI/UX）
- 文章力（コンテンツ作成）

**技術者向け**:
- TypeScript/React
- Python/FastAPI
- データ分析（pandas, LightGBM）
- スクレイピング（BeautifulSoup, httpx）

### コントリビューションガイド

`CONTRIBUTING.md`:
```markdown
# 貢献の方法

## コードを書く
1. Issueを確認、または新規作成
2. Forkしてブランチ作成
3. コード変更とテスト
4. Pull Requestを送る

## ドキュメントを改善
誤字脱字、わかりにくい説明の修正大歓迎

## 他競馬場版を作る
「〇〇競馬版作りました！」報告をIssueで共有

## アイデアを提案
「こんな機能があったら」をDiscussionsで提案
```

## ロードマップ

### フェーズ1: 金沢版の完成（現在）
- 全機能実装
- 安定稼働
- ドキュメント整備

### フェーズ2: 汎用化（3ヶ月後）
- 設定ファイルで競馬場切り替え
- 汎用スクレイパー実装
- カスタマイズガイド作成

### フェーズ3: オープンソース公開（6ヶ月後）
- GitHub公開（MITライセンス）
- README整備
- コミュニティ立ち上げ

### フェーズ4: 他競馬場での展開（1年後）
- 大井競馬版（東京のファンが作成？）
- 笠松競馬版（岐阜のファンが作成？）
- 各競馬場で立ち上がり始める

### フェーズ5: エコシステム形成（2年後）
- 全15競馬場でファンサイトが稼働
- ベストプラクティス共有
- 地方競馬全体の認知度アップ

## ビジネスモデル（非営利）

### 基本方針
- **完全無料**: ユーザーに課金しない
- **広告なし**: 煩わしい広告を表示しない
- **アフィリエイト**: 楽天競馬のみ（競馬場への貢献）

### 運営コスト
- ホスティング: 月額0〜500円（無料枠で十分）
- ドメイン: 年額1,000円程度
- → 個人で十分負担可能

### 収益化（オプション）
- 楽天競馬アフィリエイト（競馬場への還元目的）
- スポンサー広告（競馬関連企業のみ）
- 寄付（Patreon等）

## 法的・倫理的配慮

### データ利用規約の遵守
- NAR公式の利用規約を確認
- スクレイピングの頻度制限
- robots.txt の遵守

### 著作権
- レース名、馬名等は事実情報（著作権なし）
- 公式画像・ロゴの無断使用は避ける
- オリジナルコンテンツを作成

### 責任の明確化
- 予想は「参考情報」であることを明示
- 「必ず当たる」等の誤認表現禁止
- ギャンブル依存への注意喚起

## 成功指標（KPI）

### 短期（1年）
- GitHub Stars: 100以上
- 他競馬場版の立ち上げ: 3箇所以上
- コントリビューター: 10人以上

### 中期（3年）
- 全15競馬場のうち10箇所でサイト稼働
- 月間訪問者: 各サイト10,000人以上
- 地方競馬の売上に貢献（測定は難しいが）

### 長期（5年）
- 地方競馬のファンベース拡大
- 廃止危機の競馬場を救う
- 中央競馬ファンが地方競馬にも興味を持つきっかけに

## 他のオープンソースプロジェクトからの学び

### 成功例
- **WordPress**: 誰でもブログを作れる
- **Mastodon**: 誰でもSNSインスタンスを立てられる
- **Ghost**: 誰でもニュースサイトを作れる

### 参考にすべき点
- ドキュメントの充実
- 初心者でも始められる
- カスタマイズしやすい設計
- アクティブなコミュニティ

## まとめ

**「金沢競馬で成功したノウハウを、全国の地方競馬ファンに届ける」**

このプロジェクトをオープンソース化することで:
1. 他の競馬場でも同様のファンサイトが立ち上がる
2. 地方競馬全体が盛り上がる
3. 各競馬場の存続に貢献する
4. ファン同士の交流が生まれる

技術的な障壁を下げ、情熱あるファンが自分の競馬場を盛り上げられるようにする。

**地方競馬を、みんなの力で守ろう。**
