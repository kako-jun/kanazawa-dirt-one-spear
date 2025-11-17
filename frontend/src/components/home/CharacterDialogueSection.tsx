export default function CharacterDialogueSection() {
  return (
    <section className="py-12 md:py-16 bg-gradient-to-br from-retro-blue/10 to-retro-wheat">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl md:text-4xl font-serif font-bold text-retro-brown text-center mb-4">
          AI予想の10の作戦
        </h2>
        <p className="text-center text-retro-dark-gray mb-8">
          アヤメとアルゴが、異なる予想アプローチを分かりやすく解説
        </p>

        {/* キャラクター紹介 */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {/* アヤメ */}
          <div className="newspaper-card p-6">
            <div className="flex items-start gap-4">
              <div className="w-20 h-20 rounded-full bg-retro-wheat border-3 border-retro-brown flex items-center justify-center text-4xl flex-shrink-0">
                👩‍🔬
              </div>
              <div>
                <h3 className="text-xl font-bold text-retro-brown mb-2">
                  アヤメ（分析担当）
                </h3>
                <p className="text-sm text-retro-dark-gray mb-2">
                  真面目で分析好きなデータサイエンティスト。
                  難しい統計やアルゴリズムを分かりやすく説明してくれる。
                </p>
                <div className="text-xs text-retro-brown italic">
                  「統計って面白いでしょ？グラフで見ると分かりやすいよね！」
                </div>
              </div>
            </div>
          </div>

          {/* アルゴ */}
          <div className="newspaper-card p-6">
            <div className="flex items-start gap-4">
              <div className="w-20 h-20 rounded-full bg-retro-blue/20 border-3 border-retro-blue flex items-center justify-center text-4xl flex-shrink-0">
                🤖
              </div>
              <div>
                <h3 className="text-xl font-bold text-retro-blue mb-2">
                  アルゴ（AI擬人化）
                </h3>
                <p className="text-sm text-retro-dark-gray mb-2">
                  冷静沈着なAI。論理的に予想を導き出すが、
                  時々人間らしい疑問も持つアヤメの相棒。
                </p>
                <div className="text-xs text-retro-blue italic">
                  「僕の予想は過去のデータから学んだ結果さ。」
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* 作戦サンプル: 王道・勝率予測型 */}
        <div className="newspaper-card p-6 md:p-8 bg-white">
          <div className="text-sm text-retro-blue mb-2 text-center">作戦サンプル</div>
          <h3 className="text-2xl font-serif font-bold text-retro-brown mb-6 text-center">
            🎯 作戦1「王道・勝率予測型」
          </h3>

          {/* 会話 */}
          <div className="space-y-4 max-w-3xl mx-auto">
            {/* アヤメのセリフ */}
            <div className="flex gap-3 items-start">
              <div className="w-12 h-12 rounded-full bg-retro-blue border-2 border-retro-blue flex items-center justify-center text-2xl flex-shrink-0">
                👩‍🔬
              </div>
              <div className="flex-1">
                <div className="bg-white p-4 rounded-lg shadow-sm text-sm text-retro-dark-gray leading-relaxed border-2 border-retro-blue/20">
                  「まずは基本から！各馬が1着になる確率を予測して、
                  上位3頭を3連単として選ぶ方法だよ。
                  LightGBMっていう機械学習モデルで、過去の成績・騎手・馬場状態を学習するの。」
                </div>
              </div>
            </div>

            {/* アルゴのセリフ */}
            <div className="flex gap-3 items-start">
              <div className="w-12 h-12 rounded-full bg-retro-crimson border-2 border-retro-crimson flex items-center justify-center text-2xl flex-shrink-0">
                🤖
              </div>
              <div className="flex-1">
                <div className="bg-white p-4 rounded-lg shadow-sm text-sm text-retro-dark-gray leading-relaxed border-2 border-retro-crimson/20">
                  「僕が見てるのは、馬の過去勝率、騎手の成績、距離適性、馬場状態...
                  約30個の特徴量だ。8,718レースのデータから学習して、
                  『この馬は15%の確率で勝つ』って予測するんだ。」
                </div>
              </div>
            </div>

            {/* アヤメのセリフ */}
            <div className="flex gap-3 items-start">
              <div className="w-12 h-12 rounded-full bg-retro-blue border-2 border-retro-blue flex items-center justify-center text-2xl flex-shrink-0">
                👩‍🔬
              </div>
              <div className="flex-1">
                <div className="bg-white p-4 rounded-lg shadow-sm text-sm text-retro-dark-gray leading-relaxed border-2 border-retro-blue/20">
                  「ただし注意点があるの。1着を当てるのと、3連単を当てるのは別問題。
                  1着の予測精度が高くても、2着・3着の順番まで当てるのは難しい...
                  でも、これが基本中の基本だから、まずはここから！」
                </div>
              </div>
            </div>
          </div>

          {/* 学べるポイント */}
          <div className="mt-6 bg-retro-blue/10 p-4 rounded-lg border-l-4 border-retro-blue">
            <div className="font-bold text-retro-brown mb-2">📚 学習ポイント</div>
            <ul className="text-sm text-retro-dark-gray space-y-1">
              <li>• LightGBMは決定木を組み合わせた機械学習モデル</li>
              <li>• クラス不均衡（1/8の馬しか勝たない）が課題</li>
              <li>• 1着予測と3連単予想は別のアプローチが必要</li>
            </ul>
          </div>
        </div>

        {/* 他の9つの作戦へのリンク */}
        <div className="mt-8 newspaper-card p-6 bg-retro-gold/10">
          <h3 className="text-lg font-bold text-retro-brown mb-3 text-center">
            残り9つの作戦
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3 mb-4 text-sm">
            <div className="p-2 bg-white rounded">2. 順位予測型</div>
            <div className="p-2 bg-white rounded">3. 穴馬ハンター</div>
            <div className="p-2 bg-white rounded">4. 相性重視型</div>
            <div className="p-2 bg-white rounded">5. 条件スペシャリスト</div>
            <div className="p-2 bg-white rounded">6. 展開予想型</div>
            <div className="p-2 bg-white rounded">7. 三連単パターン</div>
            <div className="p-2 bg-white rounded">8. 三連組合せ</div>
            <div className="p-2 bg-white rounded">9. オッズ無視型</div>
            <div className="p-2 bg-white rounded">10. オッズ考慮型</div>
          </div>
          <div className="text-center">
            <a
              href="/strategies"
              className="inline-block px-8 py-4 bg-retro-brown text-white rounded-lg font-bold text-lg hover:bg-opacity-90 transition-colors shadow-retro"
            >
              10の作戦をすべて見る
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}
