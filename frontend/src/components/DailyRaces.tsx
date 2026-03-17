'use client'

import { useState, useEffect } from 'react'
import { Race, Prediction, apiClient } from '@/lib/api-client'
import SpearPrediction from './SpearPrediction'

interface DailyRacesProps {
  date: string
  onBack: () => void
}

interface RaceWithPrediction {
  race: Race
  prediction: Prediction | null
}

export default function DailyRaces({ date, onBack }: DailyRacesProps) {
  const [races, setRaces] = useState<RaceWithPrediction[]>([])
  const [selectedRace, setSelectedRace] = useState<RaceWithPrediction | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchDailyRaces = async () => {
      try {
        setLoading(true)

        const raceList = await apiClient.getRaces(date)

        const racesWithPredictions = await Promise.all(
          raceList.map(async (race) => {
            try {
              const prediction = await apiClient.getPrediction(race.race_id)
              return { race, prediction }
            } catch {
              return { race, prediction: null }
            }
          })
        )

        // 確度順にソート
        racesWithPredictions.sort((a, b) => {
          const confA = a.prediction?.confidence || 0
          const confB = b.prediction?.confidence || 0
          return confB - confA
        })

        setRaces(racesWithPredictions)
      } catch (error) {
        console.error('Failed to fetch daily races:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchDailyRaces()
  }, [date])

  const formatDate = (dateStr: string) => {
    const d = new Date(dateStr)
    return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`
  }

  const topRace = races.length > 0 ? races[0] : null

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-retro-sepia">
        <div className="text-base text-retro-brown font-mono">読み込み中...</div>
      </div>
    )
  }

  if (selectedRace) {
    return (
      <div className="min-h-screen bg-retro-sepia">
        <div className="p-6">
          <button
            onClick={() => setSelectedRace(null)}
            className="mb-4 px-4 py-2 font-bold text-sm rounded font-mono text-retro-wheat border border-retro-wheat opacity-70 hover:opacity-100 transition-opacity"
            style={{
              background: 'rgba(61,28,14,0.8)',
            }}
          >
            ← レース一覧に戻る
          </button>

          {/* レースヘッダー */}
          <div className="showa-sign p-5 rounded-sm mb-6">
            <div className="flex items-center gap-4 mb-2">
              <span className="horse-number-badge text-lg px-3 py-1 rounded" style={{ width: 'auto', height: 'auto' }}>
                {selectedRace.race.race_number}R
              </span>
              <h1
                className="text-2xl md:text-3xl font-serif font-black text-retro-wheat"
                style={{ textShadow: '2px 2px 4px rgba(0,0,0,0.7)' }}
              >
                {selectedRace.race.name}
              </h1>
            </div>
            <div className="flex flex-wrap gap-4 text-sm text-retro-wheat opacity-70 font-mono">
              <span>{selectedRace.race.distance}m ダート</span>
              <span>{selectedRace.race.weather}</span>
              <span>馬場: {selectedRace.race.track_condition}</span>
            </div>
          </div>

          {selectedRace.prediction && (
            <SpearPrediction
              prediction={selectedRace.prediction}
              entries={selectedRace.race.entries}
            />
          )}

          {/* 出馬表 */}
          <div className="mt-8">
            <div className="mb-4">
              <h2 className="showa-section-title text-lg">出走表</h2>
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
                  {selectedRace.race.entries.map((entry) => (
                    <tr key={entry.entry_id}>
                      <td>{entry.gate_number}</td>
                      <td>
                        <span className="horse-number-badge w-7 h-7 text-xs">{entry.horse_number}</span>
                      </td>
                      <td className="font-serif font-bold">{entry.horse.name}</td>
                      <td className="font-mono text-xs">{entry.horse.gender}{entry.horse.age}</td>
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
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-retro-sepia p-6 md:p-8">
      {/* 戻るボタン */}
      <button
        onClick={onBack}
        className="mb-6 px-4 py-2 font-bold text-sm rounded font-mono text-retro-wheat border border-retro-wheat opacity-70 hover:opacity-100 transition-opacity"
        style={{ background: 'rgba(61,28,14,0.8)' }}
      >
        ← 戻る
      </button>

      {/* タイトル看板 */}
      <div className="mb-2">
        <h1 className="showa-section-title text-xl">
          {formatDate(date)} の全レース予想
        </h1>
      </div>
      <p className="text-retro-brown opacity-70 mb-6 text-xs font-mono">
        — 最高確度のレースが購入推奨 —
      </p>

      {races.length === 0 ? (
        <div className="text-center py-20">
          <div className="text-4xl mb-4">📅</div>
          <div className="text-base text-retro-brown font-serif">
            この日のレースはありません
          </div>
        </div>
      ) : (
        <div className="space-y-3">
          {races.map((raceData, index) => {
            const isTopRace = index === 0
            const prediction = raceData.prediction

            return (
              <div
                key={raceData.race.race_id}
                onClick={() => setSelectedRace(raceData)}
                className="aged-paper-card p-5 cursor-pointer rounded-sm hover:shadow-retro transition-shadow"
                style={{
                  borderTopWidth: isTopRace ? '4px' : '2px',
                  borderTopColor: isTopRace ? '#C8102E' : '#8B5E3C',
                }}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => e.key === 'Enter' && setSelectedRace(raceData)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    {/* 購入推奨スタンプ */}
                    {isTopRace && (
                      <div
                        className="text-xs font-bold text-retro-wheat px-2 py-1 font-mono"
                        style={{
                          background: '#C8102E',
                          border: '2px solid #8B0000',
                          transform: 'rotate(-2deg)',
                          boxShadow: '2px 2px 0 rgba(0,0,0,0.3)'
                        }}
                      >
                        購入推奨
                      </div>
                    )}
                    <span className="horse-number-badge w-8 h-8 text-sm">
                      {raceData.race.race_number}
                    </span>
                    <div>
                      <div className="font-serif font-black text-retro-brown-dark text-base">
                        {raceData.race.name}
                      </div>
                      <div className="flex gap-3 text-xs text-retro-brown font-mono opacity-60 mt-0.5">
                        <span>{raceData.race.distance}m</span>
                        <span>{raceData.race.weather}</span>
                        <span>{raceData.race.track_condition}</span>
                      </div>
                    </div>
                  </div>

                  {/* 予想と確度 */}
                  {prediction ? (
                    <div className="text-right">
                      <div className="text-xs text-retro-brown mb-1 font-mono opacity-60">予想</div>
                      <div className="font-mono font-black text-retro-brown-dark text-lg tracking-wider">
                        {prediction.first}-{prediction.second}-{prediction.third}
                      </div>
                      <div
                        className={`text-xl font-black font-mono mt-1 ${
                          isTopRace ? 'text-retro-crimson' : 'text-retro-brown'
                        }`}
                      >
                        {Math.round(prediction.confidence * 100)}%
                      </div>
                    </div>
                  ) : (
                    <div className="text-xs text-retro-brown opacity-40 font-mono">予想なし</div>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      )}

      {/* 購入ルール説明 — 黒板スタイル */}
      {topRace && (
        <div className="mt-8 chalk-board p-5 rounded-sm">
          <h3 className="font-serif font-bold text-retro-chalk text-base mb-3">
            購入ルール
          </h3>
          <ul className="text-sm text-retro-chalk space-y-1 opacity-80 font-mono leading-relaxed">
            <li>• 1日に購入するのは<strong>最高確度の1レースのみ</strong></li>
            <li>
              • 今日の推奨: <strong>{topRace.race.race_number}R</strong>{' '}
              {topRace.race.name} （確度{' '}
              {Math.round((topRace.prediction?.confidence || 0) * 100)}%）
            </li>
            <li>• 三連単を100円〜購入</li>
            <li>• レース後に結果を記録</li>
          </ul>
        </div>
      )}
    </div>
  )
}
