import { Result, Statistics } from '@/lib/api-client'

interface RecentHitsSectionProps {
  results: Result[]
  statistics: Statistics | null
}

export default function RecentHitsSection({ results, statistics }: RecentHitsSectionProps) {
  const hitRate = statistics?.hit_rate || 0
  const avgPayout = statistics?.max_payout || 0

  if (!results || results.length === 0) {
    return (
      <section className="py-12 md:py-16 bg-retro-parchment">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-8">
            <h2 className="showa-section-title text-2xl md:text-3xl">
              最近の的中
            </h2>
          </div>
          <div className="betting-slip max-w-2xl mx-auto p-6 text-center text-retro-brown">
            <p>結果データがまだありません</p>
          </div>
        </div>
      </section>
    )
  }

  return (
    <section className="py-12 md:py-16 bg-retro-parchment">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <h2 className="showa-section-title text-2xl md:text-3xl">
            最近の的中
          </h2>
        </div>

        <div className="max-w-2xl mx-auto">
          <div className="betting-slip p-6 md:p-8 rounded-sm">
            {/* 掲示板風ヘッダー */}
            <div className="text-xs font-mono text-retro-brown opacity-60 text-center mb-4 tracking-widest">
              — 成績掲示板 —
            </div>

            {/* 直近の結果リスト */}
            <div className="space-y-2 mb-6">
              {results.map((result) => {
                const resultDate = new Date(result.recorded_at)
                const dateStr = `${resultDate.getMonth() + 1}/${resultDate.getDate()}`

                return (
                  <div
                    key={result.result_id}
                    className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 p-3 rounded-sm relative overflow-hidden"
                    style={{
                      background: result.prediction_hit
                        ? 'rgba(200,16,46,0.05)'
                        : 'rgba(0,0,0,0.03)',
                      border: '1px solid',
                      borderColor: result.prediction_hit
                        ? 'rgba(200,16,46,0.2)'
                        : 'rgba(139,94,60,0.2)',
                    }}
                  >
                    {/* 的中時の薄い赤背景装飾 */}
                    {result.prediction_hit && (
                      <div className="absolute inset-0 opacity-5"
                        style={{
                          background: 'repeating-diagonal-lines',
                          backgroundImage: 'repeating-linear-gradient(45deg, #C8102E, #C8102E 1px, transparent 1px, transparent 6px)'
                        }}
                      />
                    )}

                    <div className="flex items-center gap-3 relative">
                      <span className="text-xs font-bold text-retro-brown font-mono min-w-[3rem]">
                        {dateStr}
                      </span>
                      <span className="font-mono font-bold text-retro-brown-dark text-lg tracking-wider">
                        {result.first}-{result.second}-{result.third}
                      </span>
                    </div>

                    <div className="flex items-center gap-3 relative">
                      {result.prediction_hit ? (
                        <>
                          {result.payout_trifecta && (
                            <span
                              className="font-mono text-xl font-black text-retro-gold"
                              style={{ textShadow: '1px 1px 0 rgba(139,101,0,0.5)' }}
                            >
                              ¥{result.payout_trifecta.toLocaleString()}
                            </span>
                          )}
                          <div className="hit-stamp w-12 h-12 flex items-center justify-center text-xs leading-tight stamp-appear">
                            的中!
                          </div>
                        </>
                      ) : (
                        <span className="text-sm text-retro-brown-light font-mono opacity-60">不的中</span>
                      )}
                    </div>
                  </div>
                )
              })}
            </div>

            {/* 統計サマリー — LED的なデザイン */}
            <div className="border-t-2 border-dashed border-retro-wheat-dark pt-6 grid grid-cols-2 gap-4">
              <div className="text-center">
                <div className="text-xs text-retro-brown mb-1 font-bold tracking-wide">的中率</div>
                <div
                  className="text-3xl font-black text-retro-crimson font-mono"
                  style={{ textShadow: '1px 1px 0 rgba(139,0,0,0.4)' }}
                >
                  {hitRate.toFixed(1)}%
                </div>
              </div>
              <div className="text-center">
                <div className="text-xs text-retro-brown mb-1 font-bold tracking-wide">最高配当</div>
                <div
                  className="text-3xl font-black text-retro-gold font-mono"
                  style={{ textShadow: '1px 1px 0 rgba(139,101,0,0.4)' }}
                >
                  ¥{avgPayout.toLocaleString()}
                </div>
              </div>
            </div>

            {/* 詳細リンク */}
            <div className="mt-6 text-center">
              <a
                href="/history"
                className="inline-block px-6 py-3 font-bold text-retro-wheat rounded text-sm border-2 border-retro-brown"
                style={{
                  background: 'linear-gradient(180deg, #8B5E3C 0%, #6B3A2A 100%)',
                  boxShadow: '3px 3px 0 rgba(0,0,0,0.3)'
                }}
              >
                全履歴を見る
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
