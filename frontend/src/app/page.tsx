'use client'

import { useEffect, useState } from 'react'
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'
import HeroSection from '@/components/home/HeroSection'
import LatestPredictionSection from '@/components/home/LatestPredictionSection'
import RecentHitsSection from '@/components/home/RecentHitsSection'
import StatsHighlightSection from '@/components/home/StatsHighlightSection'
import RacecourseSection from '@/components/home/RacecourseSection'
import CharacterDialogueSection from '@/components/home/CharacterDialogueSection'
import { apiClient, Race, Prediction, Statistics, Result } from '@/lib/api-client'

export default function Home() {
  const [latestRace, setLatestRace] = useState<Race | null>(null)
  const [latestPrediction, setLatestPrediction] = useState<Prediction | null>(null)
  const [statistics, setStatistics] = useState<Statistics | null>(null)
  const [recentResults, setRecentResults] = useState<Result[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)

        // 並行してデータを取得
        const [races, stats, results] = await Promise.all([
          apiClient.getRaces(),
          apiClient.getStatistics(),
          apiClient.getResults(),
        ])

        // 最新のレースを取得
        if (races.length > 0) {
          const latest = races[races.length - 1]
          setLatestRace(latest)

          // 最新レースの予想を取得（エラーハンドリング付き）
          try {
            const prediction = await apiClient.getPrediction(latest.race_id)
            setLatestPrediction(prediction)
          } catch (error) {
            console.log('予想がまだ生成されていません')
          }
        }

        setStatistics(stats)
        setRecentResults(results.slice(-3).reverse()) // 最新3件を逆順
      } catch (error) {
        console.error('Failed to fetch data:', error)
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
    <div className="min-h-screen flex flex-col">
      {/* ヘッダー */}
      <Header />

      {/* メインコンテンツ */}
      <main className="flex-1">
        {/* メインビジュアル */}
        <HeroSection />

        {/* 最新AI予想 */}
        <LatestPredictionSection
          race={latestRace}
          prediction={latestPrediction}
        />

        {/* 最近の的中実績 */}
        <RecentHitsSection
          results={recentResults}
          statistics={statistics}
        />

        {/* 統計ハイライト */}
        <StatsHighlightSection statistics={statistics} />

        {/* キャラクター会話劇 */}
        <CharacterDialogueSection />

        {/* 金沢競馬場の魅力 */}
        <RacecourseSection />
      </main>

      {/* フッター */}
      <Footer />
    </div>
  )
}
