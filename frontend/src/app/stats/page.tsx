'use client'

import { useEffect, useState } from 'react'
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'
import { apiClient } from '@/lib/api-client'

interface RaceStats {
  total_races: number
  total_horses: number
  total_jockeys: number
  total_trainers: number
  track_conditions: { [key: string]: number }
  distances: { [key: string]: number }
  popularity_win_rates: { [key: string]: number }
  gate_win_rates: { [key: string]: number }
}

interface PayoutStats {
  avg_win: number
  avg_trifecta: number
  max_win: number
  max_trifecta: number
  min_win: number
  min_trifecta: number
}

export default function StatsPage() {
  const [raceStats, setRaceStats] = useState<RaceStats | null>(null)
  const [payoutStats, setPayoutStats] = useState<PayoutStats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        // TODO: バックエンドに統計APIを追加したらここで取得
        // 今はモックデータで表示
        const mockRaceStats: RaceStats = {
          total_races: 8718,
          total_horses: 12924,
          total_jockeys: 281,
          total_trainers: 308,
          track_conditions: {
            良: 4648,
            稍重: 1283,
            重: 1312,
            不良: 1475,
          },
          distances: {
            '1400m': 2800,
            '1500m': 3050,
            '1700m': 1500,
            '2000m': 800,
            その他: 568,
          },
          popularity_win_rates: {
            '1番人気': 47.84,
            '2番人気': 20.57,
            '3番人気': 12.34,
            '4番人気': 7.89,
            '5番人気': 4.23,
            '6番人気以下': 7.13,
          },
          gate_win_rates: {
            '1枠': 10.52,
            '2枠': 11.23,
            '3枠': 11.86,
            '4枠': 11.45,
            '5枠': 11.02,
            '6枠': 10.98,
            '7枠': 11.08,
            '8枠': 11.86,
          },
        }

        const mockPayoutStats: PayoutStats = {
          avg_win: 636,
          avg_trifecta: 5202,
          max_win: 43210,
          max_trifecta: 1032020,
          min_win: 100,
          min_trifecta: 180,
        }

        setRaceStats(mockRaceStats)
        setPayoutStats(mockPayoutStats)
      } catch (error) {
        console.error('Failed to fetch stats:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-retro-sepia">
        <div className="text-xl text-retro-brown">読み込み中...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex flex-col bg-retro-sepia">
      <Header />

      <main className="flex-1 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl md:text-4xl font-serif font-bold text-retro-brown mb-8">
            金沢競馬 統計データ
          </h1>

          {/* 概要サマリー */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div className="newspaper-card p-6 text-center">
              <div className="text-sm text-retro-brown mb-2 font-bold">
                総レース数
              </div>
              <div className="text-4xl font-bold font-mono text-retro-dark-gray">
                {raceStats?.total_races.toLocaleString()}
              </div>
              <div className="text-xs text-retro-brown mt-1">2015-2025年</div>
            </div>
            <div className="newspaper-card p-6 text-center">
              <div className="text-sm text-retro-brown mb-2 font-bold">
                総出走馬数
              </div>
              <div className="text-4xl font-bold font-mono text-retro-blue">
                {raceStats?.total_horses.toLocaleString()}
              </div>
              <div className="text-xs text-retro-brown mt-1">ユニーク頭数</div>
            </div>
            <div className="newspaper-card p-6 text-center">
              <div className="text-sm text-retro-brown mb-2 font-bold">騎手数</div>
              <div className="text-4xl font-bold font-mono text-retro-green">
                {raceStats?.total_jockeys}
              </div>
              <div className="text-xs text-retro-brown mt-1">延べ人数</div>
            </div>
            <div className="newspaper-card p-6 text-center">
              <div className="text-sm text-retro-brown mb-2 font-bold">
                調教師数
              </div>
              <div className="text-4xl font-bold font-mono text-retro-crimson">
                {raceStats?.total_trainers}
              </div>
              <div className="text-xs text-retro-brown mt-1">延べ人数</div>
            </div>
          </div>

          {/* 馬場状態分布 */}
          <div className="newspaper-card p-6 mb-8">
            <h2 className="text-2xl font-serif font-bold text-retro-brown mb-4">
              馬場状態分布
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {raceStats &&
                Object.entries(raceStats.track_conditions).map(([condition, count]) => {
                  const percentage = ((count / raceStats.total_races) * 100).toFixed(1)
                  const colorClass =
                    condition === '良'
                      ? 'text-retro-green'
                      : condition === '稍重'
                        ? 'text-retro-gold'
                        : condition === '重'
                          ? 'text-retro-brown'
                          : 'text-retro-dark-gray'

                  return (
                    <div key={condition} className="text-center p-4 bg-white rounded-lg">
                      <div className="text-sm text-retro-brown mb-1">{condition}</div>
                      <div className={`text-3xl font-bold font-mono ${colorClass}`}>
                        {percentage}%
                      </div>
                      <div className="text-xs text-gray-600 mt-1">
                        {count.toLocaleString()}レース
                      </div>
                    </div>
                  )
                })}
            </div>
          </div>

          {/* 距離別レース数 */}
          <div className="newspaper-card p-6 mb-8">
            <h2 className="text-2xl font-serif font-bold text-retro-brown mb-4">
              距離別レース数
            </h2>
            <div className="space-y-3">
              {raceStats &&
                Object.entries(raceStats.distances)
                  .sort((a, b) => b[1] - a[1])
                  .map(([distance, count]) => {
                    const percentage = ((count / raceStats.total_races) * 100).toFixed(1)
                    const barWidth = `${percentage}%`

                    return (
                      <div key={distance}>
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-sm font-bold text-retro-brown">
                            {distance}
                          </span>
                          <span className="text-sm text-retro-dark-gray">
                            {count.toLocaleString()}レース ({percentage}%)
                          </span>
                        </div>
                        <div className="h-6 bg-gray-200 rounded-lg overflow-hidden">
                          <div
                            className="h-full bg-retro-blue"
                            style={{ width: barWidth }}
                          />
                        </div>
                      </div>
                    )
                  })}
            </div>
          </div>

          {/* 人気別勝率 */}
          <div className="newspaper-card p-6 mb-8">
            <h2 className="text-2xl font-serif font-bold text-retro-brown mb-4">
              人気別勝率
            </h2>
            <div className="space-y-3">
              {raceStats &&
                Object.entries(raceStats.popularity_win_rates).map(
                  ([popularity, winRate]) => {
                    const barWidth = `${winRate}%`
                    const colorClass =
                      popularity === '1番人気'
                        ? 'bg-retro-crimson'
                        : popularity === '2番人気'
                          ? 'bg-retro-gold'
                          : popularity === '3番人気'
                            ? 'bg-retro-blue'
                            : 'bg-gray-400'

                    return (
                      <div key={popularity}>
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-sm font-bold text-retro-brown">
                            {popularity}
                          </span>
                          <span className="text-sm text-retro-dark-gray">
                            {winRate.toFixed(1)}%
                          </span>
                        </div>
                        <div className="h-6 bg-gray-200 rounded-lg overflow-hidden">
                          <div className={`h-full ${colorClass}`} style={{ width: barWidth }} />
                        </div>
                      </div>
                    )
                  }
                )}
            </div>
            <div className="mt-4 text-sm text-retro-brown">
              ※ 1番人気が約半分、2番人気が約2割を占める
            </div>
          </div>

          {/* 枠番別勝率 */}
          <div className="newspaper-card p-6 mb-8">
            <h2 className="text-2xl font-serif font-bold text-retro-brown mb-4">
              枠番別勝率
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {raceStats &&
                Object.entries(raceStats.gate_win_rates).map(([gate, winRate]) => (
                  <div key={gate} className="text-center p-4 bg-white rounded-lg">
                    <div className="text-sm text-retro-brown mb-1">{gate}</div>
                    <div className="text-3xl font-bold font-mono text-retro-dark-gray">
                      {winRate.toFixed(1)}%
                    </div>
                  </div>
                ))}
            </div>
            <div className="mt-4 text-sm text-retro-brown">
              ※ 枠番による有利不利はほぼ均等（10.5%-11.9%）
            </div>
          </div>

          {/* 配当統計 */}
          <div className="newspaper-card p-6 mb-8 bg-retro-gold/10">
            <h2 className="text-2xl font-serif font-bold text-retro-brown mb-4">
              配当統計
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* 単勝 */}
              <div>
                <h3 className="text-lg font-bold text-retro-brown mb-3">
                  単勝（100円あたり）
                </h3>
                <div className="space-y-2">
                  <div className="flex justify-between p-3 bg-white rounded">
                    <span className="text-sm text-retro-brown">平均配当</span>
                    <span className="font-mono font-bold text-retro-gold">
                      ¥{payoutStats?.avg_win.toLocaleString()}
                    </span>
                  </div>
                  <div className="flex justify-between p-3 bg-white rounded">
                    <span className="text-sm text-retro-brown">最高配当</span>
                    <span className="font-mono font-bold text-retro-crimson">
                      ¥{payoutStats?.max_win.toLocaleString()}
                    </span>
                  </div>
                  <div className="flex justify-between p-3 bg-white rounded">
                    <span className="text-sm text-retro-brown">最低配当</span>
                    <span className="font-mono font-bold text-retro-dark-gray">
                      ¥{payoutStats?.min_win.toLocaleString()}
                    </span>
                  </div>
                </div>
              </div>

              {/* 三連単 */}
              <div>
                <h3 className="text-lg font-bold text-retro-brown mb-3">
                  三連単（100円あたり）
                </h3>
                <div className="space-y-2">
                  <div className="flex justify-between p-3 bg-white rounded">
                    <span className="text-sm text-retro-brown">平均配当</span>
                    <span className="font-mono font-bold text-retro-gold">
                      ¥{payoutStats?.avg_trifecta.toLocaleString()}
                    </span>
                  </div>
                  <div className="flex justify-between p-3 bg-white rounded">
                    <span className="text-sm text-retro-brown">最高配当</span>
                    <span className="font-mono font-bold text-retro-crimson">
                      ¥{payoutStats?.max_trifecta.toLocaleString()}
                    </span>
                  </div>
                  <div className="flex justify-between p-3 bg-white rounded">
                    <span className="text-sm text-retro-brown">最低配当</span>
                    <span className="font-mono font-bold text-retro-dark-gray">
                      ¥{payoutStats?.min_trifecta.toLocaleString()}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* 興味深い発見 */}
          <div className="newspaper-card p-6 mb-8 bg-retro-blue/10">
            <h2 className="text-2xl font-serif font-bold text-retro-brown mb-4">
              データから見る金沢競馬の特徴
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 bg-white rounded-lg">
                <div className="flex items-start gap-3">
                  <span className="text-2xl">📊</span>
                  <div>
                    <div className="font-bold text-retro-brown mb-1">
                      1500mが人気距離
                    </div>
                    <div className="text-sm text-retro-dark-gray">
                      全レースの約35%が1500m。中距離が主流。
                    </div>
                  </div>
                </div>
              </div>

              <div className="p-4 bg-white rounded-lg">
                <div className="flex items-start gap-3">
                  <span className="text-2xl">🌞</span>
                  <div>
                    <div className="font-bold text-retro-brown mb-1">
                      良馬場が約半分
                    </div>
                    <div className="text-sm text-retro-dark-gray">
                      良馬場53%、不良馬場も17%と多様なコンディション。
                    </div>
                  </div>
                </div>
              </div>

              <div className="p-4 bg-white rounded-lg">
                <div className="flex items-start gap-3">
                  <span className="text-2xl">🎯</span>
                  <div>
                    <div className="font-bold text-retro-brown mb-1">
                      1番人気の信頼度は約48%
                    </div>
                    <div className="text-sm text-retro-dark-gray">
                      単勝で1番人気が勝つのは約半分。穴馬の可能性も十分。
                    </div>
                  </div>
                </div>
              </div>

              <div className="p-4 bg-white rounded-lg">
                <div className="flex items-start gap-3">
                  <span className="text-2xl">🎪</span>
                  <div>
                    <div className="font-bold text-retro-brown mb-1">
                      枠番はほぼ公平
                    </div>
                    <div className="text-sm text-retro-dark-gray">
                      どの枠からでも勝率10.5-11.9%とバランスが良い。
                    </div>
                  </div>
                </div>
              </div>

              <div className="p-4 bg-white rounded-lg">
                <div className="flex items-start gap-3">
                  <span className="text-2xl">💰</span>
                  <div>
                    <div className="font-bold text-retro-brown mb-1">
                      三連単平均5,202円
                    </div>
                    <div className="text-sm text-retro-dark-gray">
                      100円が平均52倍に。最高100万円超えも記録。
                    </div>
                  </div>
                </div>
              </div>

              <div className="p-4 bg-white rounded-lg">
                <div className="flex items-start gap-3">
                  <span className="text-2xl">🏇</span>
                  <div>
                    <div className="font-bold text-retro-brown mb-1">
                      11年間で12,924頭が出走
                    </div>
                    <div className="text-sm text-retro-dark-gray">
                      延べ数ではなくユニーク頭数。多様な馬たちが活躍。
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* データ期間 */}
          <div className="text-center text-sm text-retro-brown">
            <p>※ データ期間: 2015年1月 〜 2025年11月</p>
            <p className="mt-1">※ レース結果データベースに基づく統計分析</p>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}
