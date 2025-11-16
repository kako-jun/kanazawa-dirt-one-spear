export default function RecentHitsSection() {
  // TODO: 実際のデータはAPIから取得
  const recentResults = [
    { date: '11/10', race: '第5R', prediction: '7-9-1', payout: 74490, hit: true },
    { date: '11/09', race: '第8R', prediction: '3-5-2', payout: 12340, hit: true },
    { date: '11/08', race: '第2R', prediction: '1-4-6', payout: 0, hit: false },
  ]

  const stats = {
    hitRate: 62.3,
    avgPayout: 18234,
  }

  return (
    <section className="py-12 md:py-16 bg-gradient-to-br from-retro-wheat to-retro-sepia">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl md:text-4xl font-serif font-bold text-retro-brown text-center mb-8">
          最近の的中
        </h2>

        <div className="newspaper-card max-w-2xl mx-auto p-6 md:p-8">
          {/* 直近の結果 */}
          <div className="space-y-3 mb-6">
            {recentResults.map((result, index) => (
              <div
                key={index}
                className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 p-3 bg-white rounded border border-retro-brown"
              >
                <div className="flex items-center gap-3">
                  <span className="text-sm font-bold text-retro-dark-gray">
                    {result.date}
                  </span>
                  <span className="text-sm text-retro-brown">
                    {result.race}
                  </span>
                  <span className="font-mono font-bold text-retro-dark-gray">
                    {result.prediction}
                  </span>
                </div>

                <div className="flex items-center gap-3">
                  {result.hit ? (
                    <>
                      <span className="font-mono text-lg font-bold text-retro-gold">
                        ¥{result.payout.toLocaleString()}
                      </span>
                      <div className="hit-stamp w-12 h-12 flex items-center justify-center text-xs">
                        的中!
                      </div>
                    </>
                  ) : (
                    <span className="text-sm text-gray-500">不的中</span>
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* 統計サマリー */}
          <div className="border-t-2 border-retro-brown pt-6 grid grid-cols-2 gap-4">
            <div className="text-center">
              <div className="text-sm text-retro-brown mb-1">直近30日的中率</div>
              <div className="text-3xl font-bold text-retro-crimson font-mono">
                {stats.hitRate}%
              </div>
            </div>
            <div className="text-center">
              <div className="text-sm text-retro-brown mb-1">平均配当</div>
              <div className="text-3xl font-bold text-retro-gold font-mono">
                ¥{stats.avgPayout.toLocaleString()}
              </div>
            </div>
          </div>

          {/* 詳細リンク */}
          <div className="mt-6 text-center">
            <a
              href="/history"
              className="inline-block px-6 py-3 bg-retro-brown text-white rounded-lg font-bold hover:bg-opacity-90 transition-colors"
            >
              全履歴を見る
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}
