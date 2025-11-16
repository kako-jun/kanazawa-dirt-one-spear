export default function StatsHighlightSection() {
  // TODO: 実際のデータはAPIから取得
  const stats = {
    totalRaces: 8718,
    dataPeriod: '2015-2025 (11年)',
    topJockey: {
      name: '中島龍也',
      winRate: 18.2,
    },
    favoriteWinRate: 32.1,
    heavyTrackBonus: 80,
  }

  return (
    <section className="py-12 md:py-16 bg-retro-dark-gray text-retro-sepia">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl md:text-4xl font-serif font-bold text-center mb-8">
          データで見る金沢競馬
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* カード1: 総分析レース */}
          <div className="newspaper-card p-6 text-retro-dark-gray">
            <div className="text-sm mb-2 text-retro-brown font-bold">
              総分析レース
            </div>
            <div className="text-4xl md:text-5xl font-bold font-mono mb-2">
              {stats.totalRaces.toLocaleString()}
            </div>
            <div className="text-xs text-retro-brown">
              データ期間: {stats.dataPeriod}
            </div>
          </div>

          {/* カード2: トップ騎手 */}
          <div className="newspaper-card p-6 text-retro-dark-gray">
            <div className="text-sm mb-2 text-retro-brown font-bold">
              トップ騎手勝率
            </div>
            <div className="text-4xl md:text-5xl font-bold font-mono text-retro-crimson mb-2">
              {stats.topJockey.winRate}%
            </div>
            <div className="text-xs text-retro-brown">
              {stats.topJockey.name}
            </div>
          </div>

          {/* カード3: 1番人気勝率 */}
          <div className="newspaper-card p-6 text-retro-dark-gray">
            <div className="text-sm mb-2 text-retro-brown font-bold">
              1番人気勝率
            </div>
            <div className="text-4xl md:text-5xl font-bold font-mono text-retro-gold mb-2">
              {stats.favoriteWinRate}%
            </div>
            <div className="text-xs text-retro-brown">
              本命でも3回に2回は外れる
            </div>
          </div>

          {/* カード4: 馬場「重」高配当率 */}
          <div className="newspaper-card p-6 text-retro-dark-gray md:col-span-2 lg:col-span-3">
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
              <div>
                <div className="text-sm mb-2 text-retro-brown font-bold">
                  馬場「重」高配当率
                </div>
                <div className="text-4xl md:text-5xl font-bold font-mono text-retro-green">
                  +{stats.heavyTrackBonus}%
                </div>
              </div>
              <div className="text-sm text-retro-brown max-w-md">
                悪馬場では荒れやすく、高配当の可能性が通常の馬場より80%アップ。
                雨の日こそチャンス！
              </div>
            </div>
          </div>
        </div>

        {/* もっと見るリンク */}
        <div className="mt-8 text-center">
          <a
            href="/stats"
            className="inline-block px-8 py-4 bg-retro-wheat text-retro-brown rounded-lg font-bold text-lg hover:bg-retro-gold hover:text-white transition-colors"
          >
            統計データをもっと見る
          </a>
        </div>
      </div>
    </section>
  )
}
