export default function CharacterDialogueSection() {
  return (
    <section className="py-12 md:py-16 bg-retro-sepia-dark">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* セクションタイトル */}
        <div className="text-center mb-4">
          <h2 className="showa-section-title text-2xl md:text-3xl">
            AI予想の10の作戦
          </h2>
        </div>
        <p className="text-center text-retro-brown opacity-70 mb-8 text-sm font-mono">
          — アヤメとアルゴが、異なる予想アプローチを解説 —
        </p>

        {/* キャラクター紹介 */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {/* アヤメ */}
          <div className="aged-paper-card p-6 rounded-sm">
            <div className="flex items-start gap-4">
              <div
                className="w-16 h-16 rounded border-3 border-retro-brown flex items-center justify-center text-3xl flex-shrink-0"
                style={{
                  background: 'linear-gradient(135deg, #EDE0C4 0%, #C9A87A 100%)',
                  boxShadow: '2px 2px 0 rgba(0,0,0,0.25)'
                }}
              >
                👩‍🔬
              </div>
              <div>
                <h3 className="text-lg font-serif font-black text-retro-brown-dark mb-2">
                  アヤメ（分析担当）
                </h3>
                <p className="text-xs text-retro-brown mb-2 leading-relaxed">
                  真面目で分析好きなデータサイエンティスト。
                  難しい統計やアルゴリズムを分かりやすく説明してくれる。
                </p>
                <div className="text-xs text-retro-brown italic opacity-70 font-serif border-l-3 border-retro-brown pl-2">
                  「統計って面白いでしょ？グラフで見ると分かりやすいよね！」
                </div>
              </div>
            </div>
          </div>

          {/* アルゴ */}
          <div className="aged-paper-card p-6 rounded-sm">
            <div className="flex items-start gap-4">
              <div
                className="w-16 h-16 rounded border-3 border-retro-blue flex items-center justify-center text-3xl flex-shrink-0"
                style={{
                  background: 'linear-gradient(135deg, #1A3A5C 0%, #2C5F8A 100%)',
                  boxShadow: '2px 2px 0 rgba(0,0,0,0.25)'
                }}
              >
                🤖
              </div>
              <div>
                <h3 className="text-lg font-serif font-black text-retro-blue mb-2">
                  アルゴ（AI擬人化）
                </h3>
                <p className="text-xs text-retro-brown mb-2 leading-relaxed">
                  冷静沈着なAI。論理的に予想を導き出すが、
                  時々人間らしい疑問も持つアヤメの相棒。
                </p>
                <div className="text-xs text-retro-blue italic opacity-80 font-serif border-l-3 border-retro-blue pl-2">
                  「僕の予想は過去のデータから学んだ結果さ。」
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* 作戦サンプル */}
        <div className="aged-paper-card p-6 md:p-8 rounded-sm">
          {/* 作戦番号 — 小さな看板風 */}
          <div className="text-center mb-6">
            <div
              className="inline-block px-4 py-1 text-xs font-mono tracking-widest text-retro-wheat"
              style={{
                background: 'linear-gradient(180deg, #2C5F8A 0%, #1A3A5C 100%)',
                border: '2px solid #1A3A5C',
                boxShadow: '2px 2px 0 rgba(0,0,0,0.3)'
              }}
            >
              作戦サンプル
            </div>
            <h3 className="text-xl md:text-2xl font-serif font-black text-retro-brown-dark mt-3">
              作戦1「王道・勝率予測型」
            </h3>
          </div>

          {/* 会話 */}
          <div className="space-y-4 max-w-3xl mx-auto">
            {/* アヤメのセリフ */}
            <div className="flex gap-3 items-start">
              <div
                className="w-10 h-10 rounded border-2 border-retro-brown flex items-center justify-center text-xl flex-shrink-0"
                style={{ background: 'linear-gradient(135deg, #EDE0C4, #C9A87A)' }}
              >
                👩‍🔬
              </div>
              <div className="flex-1">
                <div className="text-xs text-retro-brown font-bold mb-1">アヤメ</div>
                <div
                  className="p-4 text-sm text-retro-brown-dark leading-relaxed rounded-sm"
                  style={{
                    background: '#F2E8D5',
                    borderLeft: '4px solid #8B5E3C',
                    boxShadow: '1px 1px 0 rgba(0,0,0,0.1)'
                  }}
                >
                  「まずは基本から！各馬が1着になる確率を予測して、
                  上位3頭を3連単として選ぶ方法だよ。
                  LightGBMっていう機械学習モデルで、過去の成績・騎手・馬場状態を学習するの。」
                </div>
              </div>
            </div>

            {/* アルゴのセリフ */}
            <div className="flex gap-3 items-start">
              <div
                className="w-10 h-10 rounded border-2 border-retro-blue flex items-center justify-center text-xl flex-shrink-0"
                style={{ background: 'linear-gradient(135deg, #1A3A5C, #2C5F8A)' }}
              >
                🤖
              </div>
              <div className="flex-1">
                <div className="text-xs text-retro-blue font-bold mb-1">アルゴ</div>
                <div
                  className="p-4 text-sm text-retro-brown-dark leading-relaxed rounded-sm"
                  style={{
                    background: '#F2E8D5',
                    borderLeft: '4px solid #2C5F8A',
                    boxShadow: '1px 1px 0 rgba(0,0,0,0.1)'
                  }}
                >
                  「僕が見てるのは、馬の過去勝率、騎手の成績、距離適性、馬場状態...
                  約30個の特徴量だ。8,718レースのデータから学習して、
                  『この馬は15%の確率で勝つ』って予測するんだ。」
                </div>
              </div>
            </div>

            {/* アヤメのセリフ */}
            <div className="flex gap-3 items-start">
              <div
                className="w-10 h-10 rounded border-2 border-retro-brown flex items-center justify-center text-xl flex-shrink-0"
                style={{ background: 'linear-gradient(135deg, #EDE0C4, #C9A87A)' }}
              >
                👩‍🔬
              </div>
              <div className="flex-1">
                <div className="text-xs text-retro-brown font-bold mb-1">アヤメ</div>
                <div
                  className="p-4 text-sm text-retro-brown-dark leading-relaxed rounded-sm"
                  style={{
                    background: '#F2E8D5',
                    borderLeft: '4px solid #8B5E3C',
                    boxShadow: '1px 1px 0 rgba(0,0,0,0.1)'
                  }}
                >
                  「ただし注意点があるの。1着を当てるのと、3連単を当てるのは別問題。
                  1着の予測精度が高くても、2着・3着の順番まで当てるのは難しい...
                  でも、これが基本中の基本だから、まずはここから！」
                </div>
              </div>
            </div>
          </div>

          {/* 学習ポイント — 黒板スタイル */}
          <div className="mt-6 chalk-board p-4 rounded-sm">
            <div className="font-bold text-retro-chalk mb-2 font-serif text-sm tracking-wide">
              学習ポイント
            </div>
            <ul className="text-xs text-retro-chalk space-y-1 opacity-90 font-mono">
              <li>• LightGBMは決定木を組み合わせた機械学習モデル</li>
              <li>• クラス不均衡（1/8の馬しか勝たない）が課題</li>
              <li>• 1着予測と3連単予想は別のアプローチが必要</li>
            </ul>
          </div>
        </div>

        {/* 他の9つの作戦へのリンク */}
        <div className="mt-8 aged-paper-card p-6 rounded-sm">
          <h3
            className="text-base font-serif font-black text-retro-brown-dark mb-4 text-center"
          >
            残り9つの作戦
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-2 mb-6 text-xs">
            {[
              '2. 順位予測型',
              '3. 穴馬ハンター',
              '4. 相性重視型',
              '5. 条件スペシャリスト',
              '6. 展開予想型',
              '7. 三連単パターン',
              '8. 三連組合せ',
              '9. オッズ無視型',
              '10. オッズ考慮型',
            ].map((label) => (
              <div
                key={label}
                className="p-2 text-center font-mono text-retro-brown"
                style={{
                  background: '#F2E8D5',
                  border: '1px solid rgba(139,94,60,0.3)',
                  boxShadow: '1px 1px 0 rgba(0,0,0,0.1)'
                }}
              >
                {label}
              </div>
            ))}
          </div>
          <div className="text-center">
            <a
              href="/strategies"
              className="inline-block px-8 py-4 font-black text-lg rounded text-retro-wheat border-2 border-retro-brown-dark"
              style={{
                background: 'linear-gradient(180deg, #8B5E3C 0%, #6B3A2A 60%, #5A2D1A 100%)',
                boxShadow: '4px 4px 0 rgba(0,0,0,0.35)',
                textShadow: '1px 1px 2px rgba(0,0,0,0.5)'
              }}
            >
              10の作戦をすべて見る
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}
