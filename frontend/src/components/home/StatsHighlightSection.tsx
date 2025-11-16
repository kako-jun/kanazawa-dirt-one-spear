import { Statistics } from '@/lib/api-client'

interface StatsHighlightSectionProps {
  statistics: Statistics | null
}

export default function StatsHighlightSection({ statistics }: StatsHighlightSectionProps) {
  // データがない場合はデフォルト値
  const totalRaces = statistics?.total_races || 0
  const totalPredictions = statistics?.total_predictions || 0
  const hitRate = statistics?.hit_rate || 0

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
              {totalRaces.toLocaleString()}
            </div>
            <div className="text-xs text-retro-brown">
              データ期間: 2015-2025 (11年)
            </div>
          </div>

          {/* カード2: 総予想数 */}
          <div className="newspaper-card p-6 text-retro-dark-gray">
            <div className="text-sm mb-2 text-retro-brown font-bold">
              AI予想数
            </div>
            <div className="text-4xl md:text-5xl font-bold font-mono text-retro-blue mb-2">
              {totalPredictions.toLocaleString()}
            </div>
            <div className="text-xs text-retro-brown">
              AIによる予想生成数
            </div>
          </div>

          {/* カード3: 的中率 */}
          <div className="newspaper-card p-6 text-retro-dark-gray">
            <div className="text-sm mb-2 text-retro-brown font-bold">
              AI的中率
            </div>
            <div className="text-4xl md:text-5xl font-bold font-mono text-retro-crimson mb-2">
              {hitRate.toFixed(1)}%
            </div>
            <div className="text-xs text-retro-brown">
              三連単一点予想の的中率
            </div>
          </div>

          {/* カード4: データベース情報 */}
          <div className="newspaper-card p-6 text-retro-dark-gray md:col-span-2 lg:col-span-3">
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
              <div>
                <div className="text-sm mb-2 text-retro-brown font-bold">
                  データベース規模
                </div>
                <div className="text-2xl md:text-3xl font-bold font-mono text-retro-green">
                  8,718レース / 12,924頭
                </div>
              </div>
              <div className="text-sm text-retro-brown max-w-md">
                2015年から2025年までの金沢競馬データを分析。
                馬場状態、騎手、距離などあらゆる要素を考慮した予想を生成します。
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
