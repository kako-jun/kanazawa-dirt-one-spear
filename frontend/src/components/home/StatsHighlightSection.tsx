import { Statistics } from '@/lib/api-client'

interface StatsHighlightSectionProps {
  statistics: Statistics | null
}

export default function StatsHighlightSection({ statistics }: StatsHighlightSectionProps) {
  const totalRaces = statistics?.total_races || 0
  const totalPredictions = statistics?.total_predictions || 0
  const hitRate = statistics?.hit_rate || 0

  return (
    <section className="py-12 md:py-16 bg-retro-slate text-retro-sepia relative overflow-hidden">
      {/* ダート風テクスチャ背景 */}
      <div className="absolute inset-0 opacity-10"
        style={{
          backgroundImage: `
            radial-gradient(ellipse at 20% 40%, rgba(155,101,67,0.8) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 60%, rgba(107,58,42,0.6) 0%, transparent 50%)
          `
        }}
      />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* セクションタイトル */}
        <div className="text-center mb-8">
          <h2 className="showa-section-title text-2xl md:text-3xl">
            データで見る金沢競馬
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* カード1: 総分析レース */}
          <div className="aged-paper-card p-6 text-retro-brown-dark rounded-sm">
            <div className="text-xs mb-3 text-retro-brown font-bold tracking-widest uppercase font-mono">
              総分析レース
            </div>
            <div
              className="text-4xl md:text-5xl font-black font-mono mb-2 text-retro-brown-dark"
              style={{ textShadow: '2px 2px 0 rgba(0,0,0,0.2)' }}
            >
              {totalRaces.toLocaleString()}
            </div>
            <div className="text-xs text-retro-brown opacity-70 font-mono">
              データ期間: 2015-2025 (11年)
            </div>
          </div>

          {/* カード2: 総予想数 */}
          <div className="aged-paper-card p-6 rounded-sm">
            <div className="text-xs mb-3 text-retro-brown font-bold tracking-widest uppercase font-mono">
              予想数
            </div>
            <div
              className="text-4xl md:text-5xl font-black font-mono text-retro-blue mb-2"
              style={{ textShadow: '2px 2px 0 rgba(0,0,0,0.2)' }}
            >
              {totalPredictions.toLocaleString()}
            </div>
            <div className="text-xs text-retro-brown opacity-70 font-mono">
              オッズ順モデルによる予想生成数
            </div>
          </div>

          {/* カード3: 的中率 */}
          <div className="aged-paper-card p-6 rounded-sm">
            <div className="text-xs mb-3 text-retro-brown font-bold tracking-widest uppercase font-mono">
              的中率
            </div>
            <div
              className="text-4xl md:text-5xl font-black font-mono text-retro-crimson mb-2"
              style={{ textShadow: '2px 2px 0 rgba(0,0,0,0.2)' }}
            >
              {hitRate.toFixed(1)}%
            </div>
            <div className="text-xs text-retro-brown opacity-70 font-mono">
              三連単一点予想の的中率
            </div>
          </div>

          {/* カード4: DB規模 — LED電光掲示板風 */}
          <div className="md:col-span-2 lg:col-span-3">
            <div className="led-display rounded-sm py-6 px-8">
              <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                  <div className="text-xs mb-2 text-retro-gold opacity-70 tracking-widest font-mono">
                    DATABASE SIZE
                  </div>
                  <div
                    className="text-2xl md:text-3xl font-black font-mono led-flicker"
                    style={{ letterSpacing: '0.05em' }}
                  >
                    8,718 RACES / 12,924 HORSES
                  </div>
                </div>
                <div className="text-sm text-retro-gold opacity-70 max-w-md text-center sm:text-right font-mono text-xs leading-relaxed">
                  2015年から2025年までの<br />
                  金沢競馬データを分析中
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* もっと見るリンク */}
        <div className="mt-8 text-center">
          <a
            href="/stats"
            className="inline-block px-8 py-4 font-bold text-lg rounded text-retro-wheat border-2 border-retro-gold-dark"
            style={{
              background: 'linear-gradient(180deg, #C9920A 0%, #8B6500 100%)',
              boxShadow: '4px 4px 0 rgba(0,0,0,0.4)',
              textShadow: '1px 1px 2px rgba(0,0,0,0.5)'
            }}
          >
            統計データをもっと見る
          </a>
        </div>
      </div>
    </section>
  )
}
