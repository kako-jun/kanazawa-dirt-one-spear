'use client'

import { useEffect, useState } from 'react'
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'
import { apiClient, Result, Race } from '@/lib/api-client'

export default function HistoryPage() {
  const [results, setResults] = useState<Result[]>([])
  const [races, setRaces] = useState<Race[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<'all' | 'hit' | 'miss' | 'purchased'>('all')

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        const [resultsData, racesData] = await Promise.all([
          apiClient.getResults(),
          apiClient.getRaces(),
        ])
        setResults(resultsData.reverse()) // 新しい順
        setRaces(racesData)
      } catch (error) {
        console.error('Failed to fetch data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  // レースIDから詳細情報を取得
  const getRaceInfo = (raceId: string) => {
    return races.find((r) => r.race_id === raceId)
  }

  // フィルター適用
  const filteredResults = results.filter((result) => {
    if (filter === 'hit') return result.prediction_hit
    if (filter === 'miss') return !result.prediction_hit
    if (filter === 'purchased') return result.purchased
    return true
  })

  // 統計計算
  const totalResults = results.length
  const hitCount = results.filter((r) => r.prediction_hit).length
  const hitRate = totalResults > 0 ? (hitCount / totalResults) * 100 : 0

  const purchasedResults = results.filter((r) => r.purchased)
  const purchasedHitCount = purchasedResults.filter((r) => r.prediction_hit).length
  const purchasedHitRate =
    purchasedResults.length > 0
      ? (purchasedHitCount / purchasedResults.length) * 100
      : 0
  const totalInvestment = purchasedResults.reduce((sum, r) => sum + (r.bet_amount || 0), 0)
  const totalReturn = purchasedResults.reduce((sum, r) => sum + (r.return_amount || 0), 0)
  const profit = totalReturn - totalInvestment
  const roi = totalInvestment > 0 ? (totalReturn / totalInvestment) * 100 : 0

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
            予想履歴・結果
          </h1>

          {/* 統計サマリー */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div className="newspaper-card p-4 text-center">
              <div className="text-sm text-retro-brown mb-1">総予想数</div>
              <div className="text-3xl font-bold font-mono text-retro-dark-gray">
                {totalResults}
              </div>
            </div>
            <div className="newspaper-card p-4 text-center">
              <div className="text-sm text-retro-brown mb-1">的中数</div>
              <div className="text-3xl font-bold font-mono text-retro-crimson">
                {hitCount}
              </div>
            </div>
            <div className="newspaper-card p-4 text-center">
              <div className="text-sm text-retro-brown mb-1">的中率</div>
              <div className="text-3xl font-bold font-mono text-retro-gold">
                {hitRate.toFixed(1)}%
              </div>
            </div>
            <div className="newspaper-card p-4 text-center">
              <div className="text-sm text-retro-brown mb-1">購入数</div>
              <div className="text-3xl font-bold font-mono text-retro-blue">
                {purchasedResults.length}
              </div>
            </div>
          </div>

          {/* 実購入の統計 */}
          {purchasedResults.length > 0 && (
            <div className="newspaper-card p-6 mb-8 bg-retro-blue/10">
              <h2 className="text-xl font-serif font-bold text-retro-brown mb-4">
                実購入の成績
              </h2>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                <div className="text-center">
                  <div className="text-sm text-retro-brown mb-1">購入的中率</div>
                  <div className="text-2xl font-bold font-mono text-retro-crimson">
                    {purchasedHitRate.toFixed(1)}%
                  </div>
                </div>
                <div className="text-center">
                  <div className="text-sm text-retro-brown mb-1">総投資額</div>
                  <div className="text-2xl font-bold font-mono">
                    ¥{totalInvestment.toLocaleString()}
                  </div>
                </div>
                <div className="text-center">
                  <div className="text-sm text-retro-brown mb-1">総払戻額</div>
                  <div className="text-2xl font-bold font-mono text-retro-gold">
                    ¥{totalReturn.toLocaleString()}
                  </div>
                </div>
                <div className="text-center">
                  <div className="text-sm text-retro-brown mb-1">収支</div>
                  <div
                    className={`text-2xl font-bold font-mono ${
                      profit >= 0 ? 'text-retro-green' : 'text-retro-crimson'
                    }`}
                  >
                    {profit >= 0 ? '+' : ''}¥{profit.toLocaleString()}
                  </div>
                </div>
                <div className="text-center">
                  <div className="text-sm text-retro-brown mb-1">回収率</div>
                  <div className="text-2xl font-bold font-mono text-retro-blue">
                    {roi.toFixed(1)}%
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* フィルター */}
          <div className="mb-6 flex gap-3 flex-wrap">
            <button
              onClick={() => setFilter('all')}
              className={`px-4 py-2 rounded-lg font-bold transition-colors ${
                filter === 'all'
                  ? 'bg-retro-brown text-white'
                  : 'bg-white text-retro-brown border-2 border-retro-brown'
              }`}
            >
              全て ({results.length})
            </button>
            <button
              onClick={() => setFilter('hit')}
              className={`px-4 py-2 rounded-lg font-bold transition-colors ${
                filter === 'hit'
                  ? 'bg-retro-crimson text-white'
                  : 'bg-white text-retro-crimson border-2 border-retro-crimson'
              }`}
            >
              的中 ({hitCount})
            </button>
            <button
              onClick={() => setFilter('miss')}
              className={`px-4 py-2 rounded-lg font-bold transition-colors ${
                filter === 'miss'
                  ? 'bg-gray-600 text-white'
                  : 'bg-white text-gray-600 border-2 border-gray-600'
              }`}
            >
              不的中 ({totalResults - hitCount})
            </button>
            <button
              onClick={() => setFilter('purchased')}
              className={`px-4 py-2 rounded-lg font-bold transition-colors ${
                filter === 'purchased'
                  ? 'bg-retro-blue text-white'
                  : 'bg-white text-retro-blue border-2 border-retro-blue'
              }`}
            >
              実購入 ({purchasedResults.length})
            </button>
          </div>

          {/* 履歴テーブル */}
          <div className="newspaper-card p-6">
            {filteredResults.length === 0 ? (
              <div className="text-center text-retro-brown py-8">
                該当するデータがありません
              </div>
            ) : (
              <div className="space-y-3">
                {filteredResults.map((result) => {
                  const race = getRaceInfo(result.race_id)
                  const resultDate = new Date(result.recorded_at)
                  const dateStr = `${resultDate.getFullYear()}/${
                    resultDate.getMonth() + 1
                  }/${resultDate.getDate()}`

                  return (
                    <div
                      key={result.result_id}
                      className="border-2 border-retro-brown rounded-lg p-4 bg-white"
                    >
                      <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
                        {/* 左側：レース情報 */}
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="text-sm font-bold text-retro-dark-gray">
                              {dateStr}
                            </span>
                            {race && (
                              <span className="text-sm text-retro-brown">
                                {race.name}
                              </span>
                            )}
                          </div>
                          <div className="flex items-center gap-3">
                            <span className="text-lg font-mono font-bold text-retro-dark-gray">
                              {result.first}-{result.second}-{result.third}
                            </span>
                            {result.payout_trifecta && (
                              <span className="text-base font-mono font-bold text-retro-gold">
                                ¥{result.payout_trifecta.toLocaleString()}
                              </span>
                            )}
                          </div>
                        </div>

                        {/* 右側：ステータス */}
                        <div className="flex items-center gap-3">
                          {result.purchased && (
                            <span className="px-3 py-1 bg-retro-blue text-white text-sm font-bold rounded">
                              購入済
                            </span>
                          )}
                          {result.prediction_hit ? (
                            <div className="hit-stamp w-16 h-16 flex items-center justify-center text-sm">
                              的中!
                            </div>
                          ) : (
                            <span className="text-gray-500">不的中</span>
                          )}
                        </div>
                      </div>

                      {/* 購入情報 */}
                      {result.purchased && (
                        <div className="mt-3 pt-3 border-t border-retro-brown/30 text-sm">
                          <div className="flex gap-4">
                            {result.bet_amount && (
                              <span>
                                投資: ¥{result.bet_amount.toLocaleString()}
                              </span>
                            )}
                            {result.return_amount && (
                              <span className="text-retro-gold">
                                払戻: ¥{result.return_amount.toLocaleString()}
                              </span>
                            )}
                          </div>
                          {result.memo && (
                            <div className="mt-2 text-retro-brown italic">
                              {result.memo}
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  )
                })}
              </div>
            )}
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}
