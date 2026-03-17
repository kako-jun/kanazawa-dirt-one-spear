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
    <div className="min-h-screen bg-retro-sepia">
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

      {/* ヘッダー — 昭和看板スタイル */}
      <div className="showa-sign p-6">
        <div className="flex items-center justify-between mb-4">
          <button
            onClick={onBack}
            className="px-4 py-2 text-retro-wheat font-bold text-sm rounded border border-retro-wheat opacity-70 hover:opacity-100 transition-opacity font-mono"
            aria-label="レース一覧に戻る"
          >
            ← 戻る
          </button>

          <button
            onClick={() => setShowResultForm(true)}
            className="px-5 py-2 font-bold text-sm rounded text-retro-wheat border-2 border-retro-green"
            style={{
              background: 'linear-gradient(180deg, #2E6B2E 0%, #1E4A1E 100%)',
              boxShadow: '2px 2px 0 rgba(0,0,0,0.4)'
            }}
          >
            結果を記録する
          </button>
        </div>

        <div className="flex items-center gap-4 mb-2">
          <div
            className="horse-number-badge text-lg px-4 py-2 rounded"
            style={{ width: 'auto', height: 'auto', fontSize: '1.1rem' }}
          >
            {race.race_number}R
          </div>
          <h1
            className="text-2xl md:text-3xl font-serif font-black text-retro-wheat"
            style={{ textShadow: '2px 2px 4px rgba(0,0,0,0.7)' }}
          >
            {race.name}
          </h1>
        </div>

        <div className="flex flex-wrap gap-4 text-sm text-retro-wheat opacity-80 font-mono">
          <div>{formatDate(race.date)}</div>
          <div>{race.distance}m ダート</div>
          <div>{race.weather}</div>
          <div>馬場: {race.track_condition}</div>
        </div>
      </div>

      {/* 予想表示 */}
      {loading && (
        <div className="flex items-center justify-center py-20">
          <div className="text-base text-retro-brown font-mono">予想を生成中...</div>
        </div>
      )}

      {error && (
        <div className="flex items-center justify-center py-20">
          <div className="text-base text-retro-crimson font-mono">{error}</div>
        </div>
      )}

      {prediction && (
        <div className="bg-retro-sepia">
          <SpearPrediction
            prediction={prediction}
            entries={race.entries}
          />
        </div>
      )}

      {/* 出馬表 */}
      <div className="p-6 mt-4">
        <div className="mb-4 flex items-center gap-3">
          <h2
            className="showa-section-title text-xl"
          >
            出走表
          </h2>
        </div>
        <div className="rounded-sm overflow-hidden" style={{ boxShadow: '4px 4px 0 rgba(0,0,0,0.2)' }}>
          <table className="race-card-table">
            <thead>
              <tr>
                <th>枠</th>
                <th>馬番</th>
                <th>馬名</th>
                <th>性齢</th>
                <th>騎手</th>
                <th>斤量</th>
                <th>オッズ</th>
              </tr>
            </thead>
            <tbody>
              {race.entries.map((entry) => (
                <tr key={entry.entry_id}>
                  <td>{entry.gate_number}</td>
                  <td>
                    <span className="horse-number-badge w-8 h-8 text-sm">
                      {entry.horse_number}
                    </span>
                  </td>
                  <td className="font-serif font-bold">{entry.horse.name}</td>
                  <td className="font-mono text-xs">
                    {entry.horse.gender}{entry.horse.age}
                  </td>
                  <td>{entry.jockey}</td>
                  <td className="font-mono">{entry.weight}kg</td>
                  <td className="font-mono text-retro-gold font-bold">
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
