export default function HeroSection() {
  return (
    <section className="relative bg-retro-dark-gray text-retro-sepia py-12 md:py-20">
      {/* セピア風オーバーレイ */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent to-retro-brown opacity-20"></div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          {/* キャッチコピー */}
          <div className="border-y-4 border-retro-wheat py-6 mb-8">
            <h2 className="text-2xl md:text-4xl font-serif font-bold leading-relaxed">
              三連単、一点勝負
            </h2>
            <p className="text-xl md:text-3xl font-serif font-bold mt-2">
              AIが選ぶ、本命の一本槍
            </p>
          </div>

          {/* サブテキスト */}
          <div className="max-w-2xl mx-auto space-y-4">
            <p className="text-base md:text-lg leading-relaxed">
              金沢競馬に特化したAI予想システム。
              <br className="hidden sm:inline" />
              膨大なデータから導き出す、三連単の一点予想。
            </p>
            <p className="text-sm md:text-base opacity-90">
              趣味・無料・応援目的のプロジェクトです
            </p>
          </div>

          {/* アクションボタン */}
          <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center items-center">
            <a
              href="/ai"
              className="retro-button px-8 py-4 rounded-lg text-lg font-bold inline-block"
            >
              最新のAI予想を見る
            </a>
            <a
              href="/stats"
              className="px-8 py-4 bg-retro-wheat text-retro-brown rounded-lg text-lg font-bold border-2 border-retro-brown hover:bg-retro-brown hover:text-retro-sepia transition-colors"
            >
              統計・的中実績
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}
