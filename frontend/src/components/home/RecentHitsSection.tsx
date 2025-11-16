import { Result, Statistics } from '@/lib/api-client'

interface RecentHitsSectionProps {
  results: Result[]
  statistics: Statistics | null
}

export default function RecentHitsSection({ results, statistics }: RecentHitsSectionProps) {
  // データがない場合はデフォルト値
  const hitRate = statistics?.hit_rate || 0
  const avgPayout = statistics?.max_payout || 0

  if (!results || results.length === 0) {
    return (
      <section className="py-12 md:py-16 bg-gradient-to-br from-retro-wheat to-retro-sepia">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl md:text-4xl font-serif font-bold text-retro-brown text-center mb-8">
            最近の的中
          </h2>
          <div className="newspaper-card max-w-2xl mx-auto p-6 md:p-8 text-center text-retro-brown">
            <p>結果データがまだありません</p>
          </div>
        </div>
      </section>
    )
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
            {results.map((result, index) => {
              const resultDate = new Date(result.recorded_at)
              const dateStr = `${resultDate.getMonth() + 1}/${resultDate.getDate()}`

              return (
                <div
                  key={result.result_id}
                  className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 p-3 bg-white rounded border border-retro-brown"
                >
                  <div className="flex items-center gap-3">
                    <span className="text-sm font-bold text-retro-dark-gray">
                      {dateStr}
                    </span>
                    <span className="font-mono font-bold text-retro-dark-gray">
                      {result.first}-{result.second}-{result.third}
                    </span>
                  </div>

                  <div className="flex items-center gap-3">
                    {result.prediction_hit ? (
                      <>
                        {result.payout_trifecta && (
                          <span className="font-mono text-lg font-bold text-retro-gold">
                            ¥{result.payout_trifecta.toLocaleString()}
                          </span>
                        )}
                        <div className="hit-stamp w-12 h-12 flex items-center justify-center text-xs">
                          的中!
                        </div>
                      </>
                    ) : (
                      <span className="text-sm text-gray-500">不的中</span>
                    )}
                  </div>
                </div>
              )
            })}
          </div>

          {/* 統計サマリー */}
          <div className="border-t-2 border-retro-brown pt-6 grid grid-cols-2 gap-4">
            <div className="text-center">
              <div className="text-sm text-retro-brown mb-1">的中率</div>
              <div className="text-3xl font-bold text-retro-crimson font-mono">
                {hitRate.toFixed(1)}%
              </div>
            </div>
            <div className="text-center">
              <div className="text-sm text-retro-brown mb-1">最高配当</div>
              <div className="text-3xl font-bold text-retro-gold font-mono">
                ¥{avgPayout.toLocaleString()}
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
