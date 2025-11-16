export default function CharacterDialogueSection() {
  return (
    <section className="py-12 md:py-16 bg-gradient-to-br from-retro-blue/10 to-retro-wheat">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl md:text-4xl font-serif font-bold text-retro-brown text-center mb-4">
          AI予想の仕組みを知ろう
        </h2>
        <p className="text-center text-retro-dark-gray mb-8">
          アヤメとアルゴが分かりやすく解説
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

        {/* 会話劇サンプル */}
        <div className="newspaper-card p-6 md:p-8 bg-white">
          <h3 className="text-xl font-serif font-bold text-retro-brown mb-6 text-center">
            第1話: AIはどうやって予想するの？
          </h3>

          {/* 会話 */}
          <div className="space-y-4 max-w-3xl mx-auto">
            {/* アヤメのセリフ */}
            <div className="flex gap-3 items-start">
              <div className="w-12 h-12 rounded-full bg-retro-wheat border-2 border-retro-brown flex items-center justify-center text-2xl flex-shrink-0">
                👩‍🔬
              </div>
              <div className="flex-1">
                <div className="bg-retro-wheat p-4 rounded-lg rounded-tl-none">
                  <p className="text-sm leading-relaxed">
                    アルゴくん、今日の予想は<strong>「7-3-5」</strong>なんだね。
                    <br />
                    どうしてその組み合わせにしたの？
                  </p>
                </div>
              </div>
            </div>

            {/* アルゴのセリフ */}
            <div className="flex gap-3 items-start flex-row-reverse">
              <div className="w-12 h-12 rounded-full bg-retro-blue/20 border-2 border-retro-blue flex items-center justify-center text-2xl flex-shrink-0">
                🤖
              </div>
              <div className="flex-1">
                <div className="bg-retro-blue/10 p-4 rounded-lg rounded-tr-none">
                  <p className="text-sm leading-relaxed">
                    僕は過去8,700レース以上のデータから学んだんだ。
                    <br />
                    <strong>7番の馬</strong>は、この馬場状態で勝率が高い。
                    <br />
                    <strong>3番</strong>は逃げ馬で、好スタートが期待できる。
                    <br />
                    <strong>5番</strong>は穴馬として組み合わせると、高配当の可能性がある。
                  </p>
                </div>
              </div>
            </div>

            {/* アヤメのセリフ */}
            <div className="flex gap-3 items-start">
              <div className="w-12 h-12 rounded-full bg-retro-wheat border-2 border-retro-brown flex items-center justify-center text-2xl flex-shrink-0">
                👩‍🔬
              </div>
              <div className="flex-1">
                <div className="bg-retro-wheat p-4 rounded-lg rounded-tl-none">
                  <p className="text-sm leading-relaxed">
                    なるほど！つまり、
                    <br />
                    <strong className="text-retro-crimson">①馬場状態</strong>、
                    <strong className="text-retro-crimson">②脚質</strong>、
                    <strong className="text-retro-crimson">③配当バランス</strong>
                    <br />
                    この3つを考えて予想してるんだね！
                  </p>
                </div>
              </div>
            </div>

            {/* アルゴのセリフ */}
            <div className="flex gap-3 items-start flex-row-reverse">
              <div className="w-12 h-12 rounded-full bg-retro-blue/20 border-2 border-retro-blue flex items-center justify-center text-2xl flex-shrink-0">
                🤖
              </div>
              <div className="flex-1">
                <div className="bg-retro-blue/10 p-4 rounded-lg rounded-tr-none">
                  <p className="text-sm leading-relaxed">
                    その通り。でも僕の予想は<strong>参考情報</strong>だよ。
                    <br />
                    最終的には、あなたの判断で馬券を買ってね。
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* 学べるポイント */}
          <div className="mt-8 border-t-2 border-retro-brown pt-6">
            <h4 className="font-bold text-retro-brown mb-3 text-center">
              この会話で学べること
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center">
                <div className="text-2xl mb-2">📊</div>
                <div className="text-sm font-bold text-retro-brown">
                  過去データの重要性
                </div>
              </div>
              <div className="text-center">
                <div className="text-2xl mb-2">🎯</div>
                <div className="text-sm font-bold text-retro-brown">
                  予想の根拠
                </div>
              </div>
              <div className="text-center">
                <div className="text-2xl mb-2">⚠️</div>
                <div className="text-sm font-bold text-retro-brown">
                  自己判断の大切さ
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* もっと見るリンク */}
        <div className="mt-8 text-center">
          <a
            href="/learn/ai"
            className="inline-block px-8 py-4 bg-retro-blue text-white rounded-lg font-bold text-lg hover:bg-opacity-90 transition-colors shadow-retro"
          >
            もっとAIの仕組みを学ぶ
          </a>
        </div>
      </div>
    </section>
  )
}
