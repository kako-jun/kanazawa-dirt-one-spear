'use client'

import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'

export default function AIPage() {
  return (
    <div className="min-h-screen flex flex-col bg-retro-sepia">
      <Header />

      <main className="flex-1 py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl md:text-4xl font-serif font-bold text-retro-brown mb-8">
            AI予想の仕組み
          </h1>

          {/* 概要 */}
          <div className="newspaper-card p-6 mb-8 bg-retro-blue/10">
            <h2 className="text-2xl font-serif font-bold text-retro-brown mb-4">
              一本槍スタイルとは
            </h2>
            <p className="text-retro-dark-gray mb-4 leading-relaxed">
              金沢ダート一本槍は、AIが
              <span className="font-bold text-retro-crimson">三連単を1点のみ予想</span>
              する大胆なスタイルです。複数の買い目を提案せず、AIが最も自信を持つ組み合わせだけを提示します。
            </p>
            <div className="bg-white p-4 rounded-lg">
              <div className="flex items-center gap-3 mb-2">
                <span className="text-3xl">🎯</span>
                <div className="font-bold text-retro-brown">
                  なぜ1点だけ？
                </div>
              </div>
              <ul className="space-y-2 text-sm text-retro-dark-gray ml-12">
                <li>✓ 複数点買いは資金効率が悪化</li>
                <li>✓ AIの判断を最も信頼できる1点に集約</li>
                <li>✓ シンプルで分かりやすい</li>
                <li>✓ 当たれば高配当</li>
              </ul>
            </div>
          </div>

          {/* 予想モデル */}
          <div className="newspaper-card p-6 mb-8">
            <h2 className="text-2xl font-serif font-bold text-retro-brown mb-4">
              予想モデル
            </h2>

            <div className="space-y-4">
              {/* LightGBM */}
              <div className="bg-white p-5 rounded-lg">
                <h3 className="text-lg font-bold text-retro-blue mb-3 flex items-center gap-2">
                  <span>🌳</span>
                  LightGBM（勾配ブースティング）
                </h3>
                <p className="text-sm text-retro-dark-gray mb-3 leading-relaxed">
                  決定木という「質問の連鎖」で答えを導く機械学習モデル。
                  <br />
                  例：「距離は1500m以上？」→「馬場は良？」→「騎手の勝率は15%以上？」...
                </p>
                <div className="bg-retro-wheat p-3 rounded text-xs">
                  <div className="font-bold text-retro-brown mb-2">特徴</div>
                  <ul className="space-y-1 text-retro-dark-gray">
                    <li>• 高速で大規模データに強い</li>
                    <li>• なぜその予想をしたか説明可能</li>
                    <li>• カテゴリ変数（馬場、騎手など）を直接扱える</li>
                  </ul>
                </div>
              </div>

              {/* ディープラーニング（将来実装予定） */}
              <div className="bg-white p-5 rounded-lg opacity-60">
                <h3 className="text-lg font-bold text-retro-crimson mb-3 flex items-center gap-2">
                  <span>🧠</span>
                  ディープラーニング（実装予定）
                </h3>
                <p className="text-sm text-retro-dark-gray mb-3 leading-relaxed">
                  人間の脳を模した多層ニューラルネットワーク。
                  複雑なパターンを自動で学習できる。
                </p>
                <div className="bg-retro-wheat p-3 rounded text-xs">
                  <div className="font-bold text-retro-brown mb-2">特徴</div>
                  <ul className="space-y-1 text-retro-dark-gray">
                    <li>• 複雑な関係性を捉えられる</li>
                    <li>• 説明が難しい（ブラックボックス）</li>
                    <li>• 大量のデータが必要</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          {/* 学習データ */}
          <div className="newspaper-card p-6 mb-8 bg-retro-green/10">
            <h2 className="text-2xl font-serif font-bold text-retro-brown mb-4">
              学習データ
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-white p-4 rounded-lg">
                <div className="text-sm text-retro-brown mb-2 font-bold">
                  データ期間
                </div>
                <div className="text-2xl font-mono font-bold text-retro-dark-gray">
                  2015年 〜 2025年
                </div>
                <div className="text-xs text-gray-600 mt-1">約11年分</div>
              </div>
              <div className="bg-white p-4 rounded-lg">
                <div className="text-sm text-retro-brown mb-2 font-bold">
                  総レース数
                </div>
                <div className="text-2xl font-mono font-bold text-retro-dark-gray">
                  8,718レース
                </div>
                <div className="text-xs text-gray-600 mt-1">金沢競馬場のみ</div>
              </div>
            </div>
          </div>

          {/* 使用する特徴量 */}
          <div className="newspaper-card p-6 mb-8">
            <h2 className="text-2xl font-serif font-bold text-retro-brown mb-4">
              AIが見ている情報（特徴量）
            </h2>

            <div className="space-y-3">
              <div className="bg-white p-4 rounded-lg">
                <h3 className="font-bold text-retro-brown mb-2 flex items-center gap-2">
                  <span>🏇</span>
                  馬の情報
                </h3>
                <div className="text-sm text-retro-dark-gray">
                  過去の成績（勝率、連対率）、距離適性、馬場適性、休養明け日数、
                  連続出走回数、年齢、性別、血統（父馬、母馬）
                </div>
              </div>

              <div className="bg-white p-4 rounded-lg">
                <h3 className="font-bold text-retro-brown mb-2 flex items-center gap-2">
                  <span>👨‍🦱</span>
                  騎手の情報
                </h3>
                <div className="text-sm text-retro-dark-gray">
                  勝率、連対率、この馬との相性、距離別成績、馬場別成績、
                  最近の調子（直近10戦の成績）
                </div>
              </div>

              <div className="bg-white p-4 rounded-lg">
                <h3 className="font-bold text-retro-brown mb-2 flex items-center gap-2">
                  <span>👔</span>
                  調教師の情報
                </h3>
                <div className="text-sm text-retro-dark-gray">
                  勝率、連対率、騎手との組み合わせ相性
                </div>
              </div>

              <div className="bg-white p-4 rounded-lg">
                <h3 className="font-bold text-retro-brown mb-2 flex items-center gap-2">
                  <span>🏟️</span>
                  レースの情報
                </h3>
                <div className="text-sm text-retro-dark-gray">
                  距離、馬場状態、天候、出走頭数、レースグレード、
                  過去の同条件レース傾向
                </div>
              </div>

              <div className="bg-white p-4 rounded-lg border-2 border-retro-gold">
                <h3 className="font-bold text-retro-brown mb-2 flex items-center gap-2">
                  <span>💰</span>
                  オッズ情報（実験中）
                </h3>
                <div className="text-sm text-retro-dark-gray mb-2">
                  単勝オッズ、複勝オッズ、人気順位
                </div>
                <div className="text-xs text-retro-crimson">
                  ※ オッズを使うと的中率は上がるが、配当が下がる傾向。
                  現在は「オッズなしモデル」を採用し、高配当を狙う方針。
                </div>
              </div>
            </div>
          </div>

          {/* 検証方法 */}
          <div className="newspaper-card p-6 mb-8 bg-retro-wheat/30">
            <h2 className="text-2xl font-serif font-bold text-retro-brown mb-4">
              予想精度の検証方法
            </h2>

            <div className="mb-4">
              <h3 className="font-bold text-retro-brown mb-3">
                🔍 時系列交差検証（Time Series Cross-Validation）
              </h3>
              <p className="text-sm text-retro-dark-gray mb-3 leading-relaxed">
                過去のデータで学習し、未来のデータで予想をテスト。
                これを繰り返すことで、実際の運用時の精度を正確に測定します。
              </p>

              <div className="bg-white p-4 rounded-lg text-xs font-mono">
                <div className="mb-2 text-retro-brown font-bold">検証スケジュール例</div>
                <div className="space-y-1 text-retro-dark-gray">
                  <div>2015-2019年で学習 → 2020年で予想テスト</div>
                  <div>2015-2020年で学習 → 2021年で予想テスト</div>
                  <div>2015-2021年で学習 → 2022年で予想テスト</div>
                  <div>...</div>
                </div>
              </div>
            </div>

            <div className="bg-retro-crimson/10 p-4 rounded-lg border-2 border-retro-crimson">
              <div className="font-bold text-retro-crimson mb-2">
                ⚠️ 重要：未来のデータは絶対に使わない
              </div>
              <p className="text-xs text-retro-dark-gray">
                「リークテスト」と呼ばれる不正な検証では、
                未来のデータで学習してしまうため精度が実態より高く見えます。
                本プロジェクトでは厳格に時系列を守った検証を行っています。
              </p>
            </div>
          </div>

          {/* 信頼度スコア */}
          <div className="newspaper-card p-6 mb-8">
            <h2 className="text-2xl font-serif font-bold text-retro-brown mb-4">
              信頼度スコアの見方
            </h2>

            <div className="space-y-3">
              <div className="flex items-center gap-4 p-4 bg-white rounded-lg">
                <div className="text-4xl">🔥</div>
                <div>
                  <div className="font-bold text-retro-crimson mb-1">
                    信頼度 80%以上
                  </div>
                  <div className="text-sm text-retro-dark-gray">
                    AIが非常に自信を持っている予想。過去データで高勝率のパターン。
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-4 p-4 bg-white rounded-lg">
                <div className="text-4xl">👍</div>
                <div>
                  <div className="font-bold text-retro-gold mb-1">
                    信頼度 60-80%
                  </div>
                  <div className="text-sm text-retro-dark-gray">
                    AIが比較的自信を持っている予想。標準的な確度。
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-4 p-4 bg-white rounded-lg">
                <div className="text-4xl">🤔</div>
                <div>
                  <div className="font-bold text-retro-blue mb-1">
                    信頼度 60%未満
                  </div>
                  <div className="text-sm text-retro-dark-gray">
                    判断が難しいレース。期待値は低め。
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-4 text-xs text-retro-brown bg-retro-wheat p-3 rounded">
              ※ 信頼度はあくまで過去データに基づく参考値です。
              必ず当たることを保証するものではありません。
            </div>
          </div>

          {/* キャラクター対話 */}
          <div className="newspaper-card p-6 mb-8 bg-gradient-to-br from-retro-wheat to-white">
            <h2 className="text-2xl font-serif font-bold text-retro-brown mb-4">
              🤖 アヤメ × アルゴの解説コーナー
            </h2>

            <div className="space-y-4">
              {/* アヤメの発言 */}
              <div className="flex gap-3">
                <div className="flex-shrink-0 w-12 h-12 bg-retro-blue rounded-full flex items-center justify-center text-2xl">
                  👩‍🔬
                </div>
                <div className="flex-1">
                  <div className="font-bold text-retro-brown mb-1">
                    アヤメ（統計分析担当）
                  </div>
                  <div className="bg-white p-4 rounded-lg shadow-sm text-sm text-retro-dark-gray leading-relaxed">
                    「LightGBMっていうのはね、決定木っていう『質問の連鎖』で答えを導くモデルなの。
                    例えば『この馬は1500m以上得意？』→『馬場は良？』→『騎手の勝率15%以上？』
                    ってどんどん絞り込んでいくイメージだよ！」
                  </div>
                </div>
              </div>

              {/* アルゴの発言 */}
              <div className="flex gap-3">
                <div className="flex-shrink-0 w-12 h-12 bg-retro-crimson rounded-full flex items-center justify-center text-2xl">
                  🤖
                </div>
                <div className="flex-1">
                  <div className="font-bold text-retro-brown mb-1">
                    アルゴ（AI擬人化）
                  </div>
                  <div className="bg-white p-4 rounded-lg shadow-sm text-sm text-retro-dark-gray leading-relaxed">
                    「僕が予想する時は、8,718レース分のパターンを瞬時に分析してるんだ。
                    人間には見えない微細な傾向も捉えられる。
                    でも、100%当たるわけじゃない。競馬には運もあるからね。」
                  </div>
                </div>
              </div>

              {/* アヤメの発言 */}
              <div className="flex gap-3">
                <div className="flex-shrink-0 w-12 h-12 bg-retro-blue rounded-full flex items-center justify-center text-2xl">
                  👩‍🔬
                </div>
                <div className="flex-1">
                  <div className="font-bold text-retro-brown mb-1">アヤメ</div>
                  <div className="bg-white p-4 rounded-lg shadow-sm text-sm text-retro-dark-gray leading-relaxed">
                    「三連単の的中率は、データ上では約3-5%程度が理論値。
                    AIでもこれを大きく超えるのは難しいの。
                    だから『一本槍』で勝負するのは、実はとても勇気のいる戦略なんだよね😊」
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* 免責事項 */}
          <div className="bg-retro-crimson/10 border-2 border-retro-crimson p-6 rounded-lg">
            <h2 className="text-xl font-bold text-retro-crimson mb-3">
              ⚠️ 重要な注意事項
            </h2>
            <ul className="space-y-2 text-sm text-retro-dark-gray">
              <li>✓ AI予想は参考情報です。必ず当たるわけではありません。</li>
              <li>✓ 馬券購入は自己責任で行ってください。</li>
              <li>✓ 余剰資金の範囲内で楽しみましょう。</li>
              <li>✓ ギャンブル依存にご注意ください。</li>
              <li>✓ 20歳未満の方は馬券を購入できません。</li>
            </ul>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}
