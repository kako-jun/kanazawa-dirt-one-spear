'use client'

import { useState, useEffect } from 'react'
import { Race, Statistics, Result, apiClient } from '@/lib/api-client'
import RaceList from '@/components/RaceList'
import RaceDetail from '@/components/RaceDetail'
import ResultHistory from '@/components/ResultHistory'

type Page = 'home' | 'race-detail' | 'stats' | 'history'

export default function Home() {
  const [currentPage, setCurrentPage] = useState<Page>('home')
  const [races, setRaces] = useState<Race[]>([])
  const [selectedRace, setSelectedRace] = useState<Race | null>(null)
  const [statistics, setStatistics] = useState<Statistics | null>(null)
  const [results, setResults] = useState<Result[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchRaces = async () => {
      try {
        setLoading(true)
        const data = await apiClient.getRaces()
        setRaces(data)
      } catch (error) {
        console.error('Failed to fetch races:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchRaces()
  }, [])

  const handleRaceSelect = async (raceId: string) => {
    try {
      const race = await apiClient.getRace(raceId)
      setSelectedRace(race)
      setCurrentPage('race-detail')
    } catch (error) {
      console.error('Failed to fetch race:', error)
    }
  }

  const handleBackToHome = () => {
    setCurrentPage('home')
    setSelectedRace(null)
  }

  const handleShowStats = async () => {
    try {
      const stats = await apiClient.getStatistics()
      setStatistics(stats)
      setCurrentPage('stats')
    } catch (error) {
      console.error('Failed to fetch statistics:', error)
    }
  }

  const handleShowHistory = async () => {
    try {
      const resultData = await apiClient.getResults()
      setResults(resultData)
      setCurrentPage('history')
    } catch (error) {
      console.error('Failed to fetch results:', error)
    }
  }

  if (currentPage === 'race-detail' && selectedRace) {
    return <RaceDetail race={selectedRace} onBack={handleBackToHome} />
  }

  if (currentPage === 'history') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-yellow-50 to-orange-50 p-8">
        <button
          onClick={handleBackToHome}
          className="mb-6 px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700"
        >
          ← 戻る
        </button>

        <h1 className="text-3xl font-bold mb-8 text-yellow-600">
          予想履歴・結果
        </h1>

        <ResultHistory results={results} races={races} />
      </div>
    )
  }

  if (currentPage === 'stats' && statistics) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-yellow-50 to-orange-50 p-8">
        <button
          onClick={handleBackToHome}
          className="mb-6 px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700"
        >
          ← 戻る
        </button>

        <h1 className="text-3xl font-bold mb-8 text-yellow-600">
          的中実績・統計
        </h1>

        {/* 直近の成績 */}
        <div className="bg-white p-6 rounded-lg shadow-lg mb-6">
          <h2 className="font-bold text-lg mb-3">直近10件の成績</h2>
          <div className="flex gap-2 text-3xl">
            {statistics.recent_results.length > 0 ? (
              statistics.recent_results.map((result, index) => (
                <span
                  key={index}
                  className={result === '◯' ? 'text-yellow-600' : 'text-gray-400'}
                >
                  {result}
                </span>
              ))
            ) : (
              <span className="text-gray-400 text-base">まだ結果がありません</span>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <div className="text-sm text-gray-600 mb-2">総予想数</div>
            <div className="text-4xl font-bold text-gray-800">
              {statistics.total_predictions}
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-lg">
            <div className="text-sm text-gray-600 mb-2">的中数</div>
            <div className="text-4xl font-bold text-yellow-600">
              {statistics.hit_count}
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-lg">
            <div className="text-sm text-gray-600 mb-2">的中率</div>
            <div className="text-4xl font-bold text-yellow-600">
              {statistics.hit_rate.toFixed(1)}%
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-lg">
            <div className="text-sm text-gray-600 mb-2">最高配当</div>
            <div className="text-4xl font-bold text-orange-600">
              ¥{statistics.max_payout.toLocaleString()}
            </div>
          </div>
        </div>

        {/* 実購入の統計 */}
        {statistics.purchased_count > 0 && (
          <>
            <h2 className="text-2xl font-bold mb-4 text-gray-800 mt-8">
              実購入の成績
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-blue-50 p-6 rounded-lg shadow-lg border-2 border-blue-300">
                <div className="text-sm text-gray-600 mb-2">購入数</div>
                <div className="text-4xl font-bold text-blue-600">
                  {statistics.purchased_count}
                </div>
              </div>

              <div className="bg-blue-50 p-6 rounded-lg shadow-lg border-2 border-blue-300">
                <div className="text-sm text-gray-600 mb-2">実購入的中率</div>
                <div className="text-4xl font-bold text-blue-600">
                  {statistics.purchased_hit_rate.toFixed(1)}%
                </div>
              </div>

              <div className="bg-blue-50 p-6 rounded-lg shadow-lg border-2 border-blue-300">
                <div className="text-sm text-gray-600 mb-2">回収率</div>
                <div className="text-4xl font-bold text-orange-600">
                  {statistics.roi.toFixed(1)}%
                </div>
              </div>

              <div className="bg-blue-50 p-6 rounded-lg shadow-lg border-2 border-blue-300">
                <div className="text-sm text-gray-600 mb-2">収支</div>
                <div
                  className={`text-4xl font-bold ${
                    statistics.profit >= 0 ? 'text-green-600' : 'text-red-600'
                  }`}
                >
                  {statistics.profit >= 0 ? '+' : ''}¥
                  {statistics.profit.toLocaleString()}
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-lg">
                <div className="text-sm text-gray-600 mb-2">総投資額</div>
                <div className="text-3xl font-bold text-gray-800">
                  ¥{statistics.total_investment.toLocaleString()}
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-lg">
                <div className="text-sm text-gray-600 mb-2">総払戻額</div>
                <div className="text-3xl font-bold text-green-600">
                  ¥{statistics.total_return.toLocaleString()}
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-yellow-50 to-orange-50">
      {/* ヘッダー */}
      <header className="bg-gradient-to-r from-yellow-600 to-orange-600 text-white p-8 shadow-lg">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-5xl font-bold mb-3 flex items-center gap-3">
            <span>⚔️</span>
            <span>金沢ダート一本槍</span>
          </h1>
          <p className="text-xl opacity-90">
            Kanazawa Dirt One Spear - AI競馬予想（3連単一本勝負）
          </p>
          <p className="text-sm mt-2 opacity-75">
            趣味・無料・金沢競馬応援プロジェクト
          </p>
        </div>
      </header>

      {/* ナビゲーション */}
      <div className="max-w-7xl mx-auto p-6">
        <div className="flex gap-4 mb-6 flex-wrap">
          <button
            onClick={() => setCurrentPage('home')}
            className={`px-6 py-3 rounded-lg font-bold transition-colors ${
              currentPage === 'home'
                ? 'bg-yellow-600 text-white'
                : 'bg-white text-gray-700 hover:bg-yellow-100'
            }`}
          >
            📋 レース一覧
          </button>
          <button
            onClick={handleShowHistory}
            className={`px-6 py-3 rounded-lg font-bold transition-colors ${
              currentPage === 'history'
                ? 'bg-yellow-600 text-white'
                : 'bg-white text-gray-700 hover:bg-yellow-100'
            }`}
          >
            📝 予想履歴
          </button>
          <button
            onClick={handleShowStats}
            className={`px-6 py-3 rounded-lg font-bold transition-colors ${
              currentPage === 'stats'
                ? 'bg-yellow-600 text-white'
                : 'bg-white text-gray-700 hover:bg-yellow-100'
            }`}
          >
            📊 的中実績
          </button>
        </div>

        {/* コンテンツ */}
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="text-xl text-gray-600">読み込み中...</div>
          </div>
        ) : (
          <RaceList races={races} onRaceSelect={handleRaceSelect} />
        )}
      </div>

      {/* フッター */}
      <footer className="mt-20 bg-gray-800 text-white p-8">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-sm mb-2">
            ※本サイトは趣味・無料・応援目的のAI予想サイトです
          </p>
          <p className="text-xs text-gray-400">
            予想は必ず当たるものではありません。ギャンブルは適度に楽しみましょう。
          </p>
        </div>
      </footer>
    </div>
  )
}
