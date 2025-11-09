'use client'

import { useState, useEffect } from 'react'
import { Race, Prediction, apiClient } from '@/lib/api-client'
import SpearPrediction from './SpearPrediction'
import ResultForm from './ResultForm'

interface RaceDetailProps {
  race: Race
  onBack: () => void
}

export default function RaceDetail({ race, onBack }: RaceDetailProps) {
  const [prediction, setPrediction] = useState<Prediction | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showResultForm, setShowResultForm] = useState(false)

  useEffect(() => {
    const fetchPrediction = async () => {
      try {
        setLoading(true)
        const pred = await apiClient.getPrediction(race.race_id)
        setPrediction(pred)
      } catch (err) {
        setError('予想データの取得に失敗しました')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchPrediction()
  }, [race.race_id])

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr)
    return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-yellow-50 to-orange-50">
      {/* 結果登録フォーム */}
      {showResultForm && (
        <ResultForm
          race={race}
          onSubmitted={() => {
            setShowResultForm(false)
            alert('結果を登録しました！')
          }}
          onCancel={() => setShowResultForm(false)}
        />
      )}

      {/* ヘッダー */}
      <div className="bg-gradient-to-r from-yellow-600 to-orange-600 text-white p-6">
        <div className="flex items-center justify-between mb-4">
          <button
            onClick={onBack}
            className="px-4 py-2 bg-white/20 hover:bg-white/30 rounded-lg transition-colors"
            aria-label="レース一覧に戻る"
          >
            ← 戻る
          </button>

          <button
            onClick={() => setShowResultForm(true)}
            className="px-6 py-3 bg-green-600 hover:bg-green-700 rounded-lg font-bold transition-colors flex items-center gap-2"
          >
            <span>📝</span>
            <span>結果を記録する</span>
          </button>
        </div>

        <div className="flex items-center gap-4 mb-2">
          <div className="bg-white text-yellow-600 px-4 py-2 rounded-full text-xl font-bold">
            {race.race_number}R
          </div>
          <h1 className="text-3xl font-bold">{race.name}</h1>
        </div>

        <div className="flex gap-6 text-sm">
          <div>📅 {formatDate(race.date)}</div>
          <div>📏 {race.distance}m ダート</div>
          <div>🌤️ {race.weather}</div>
          <div>🏇 馬場: {race.track_condition}</div>
        </div>
      </div>

      {/* 予想表示 */}
      {loading && (
        <div className="flex items-center justify-center py-20">
          <div className="text-xl text-gray-600">予想を生成中...</div>
        </div>
      )}

      {error && (
        <div className="flex items-center justify-center py-20">
          <div className="text-xl text-red-600">{error}</div>
        </div>
      )}

      {prediction && (
        <SpearPrediction
          prediction={prediction}
          entries={race.entries}
        />
      )}

      {/* 出馬表 */}
      <div className="p-6 mt-8">
        <h2 className="text-2xl font-bold mb-4 text-gray-800">出馬表</h2>
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <table className="w-full">
            <thead className="bg-yellow-600 text-white">
              <tr>
                <th className="p-3 text-left">枠</th>
                <th className="p-3 text-left">馬番</th>
                <th className="p-3 text-left">馬名</th>
                <th className="p-3 text-left">性齢</th>
                <th className="p-3 text-left">騎手</th>
                <th className="p-3 text-left">斤量</th>
                <th className="p-3 text-left">オッズ</th>
              </tr>
            </thead>
            <tbody>
              {race.entries.map((entry, index) => (
                <tr
                  key={entry.entry_id}
                  className={`border-b ${
                    index % 2 === 0 ? 'bg-gray-50' : 'bg-white'
                  } hover:bg-yellow-50`}
                >
                  <td className="p-3">{entry.gate_number}</td>
                  <td className="p-3 font-bold">{entry.horse_number}</td>
                  <td className="p-3 font-bold">{entry.horse.name}</td>
                  <td className="p-3">
                    {entry.horse.gender}
                    {entry.horse.age}
                  </td>
                  <td className="p-3">{entry.jockey}</td>
                  <td className="p-3">{entry.weight}kg</td>
                  <td className="p-3">
                    {entry.odds ? `${entry.odds.toFixed(1)}倍` : '-'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
