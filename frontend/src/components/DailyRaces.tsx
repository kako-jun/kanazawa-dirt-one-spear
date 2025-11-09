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

        // その日のレース一覧を取得
        const raceList = await apiClient.getRaces(date)

        // 各レースの予想を取得
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

  // 最高確度のレース
  const topRace = races.length > 0 ? races[0] : null

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl text-gray-600">読み込み中...</div>
      </div>
    )
  }

  if (selectedRace) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-yellow-50 to-orange-50">
        <div className="p-6">
          <button
            onClick={() => setSelectedRace(null)}
            className="mb-4 px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700"
          >
            ← レース一覧に戻る
          </button>

          <div className="bg-gradient-to-r from-yellow-600 to-orange-600 text-white p-6 rounded-lg mb-6">
            <div className="flex items-center gap-4 mb-2">
              <div className="bg-white text-yellow-600 px-4 py-2 rounded-full text-xl font-bold">
                {selectedRace.race.race_number}R
              </div>
              <h1 className="text-3xl font-bold">{selectedRace.race.name}</h1>
            </div>
            <div className="flex gap-6 text-sm">
              <div>📏 {selectedRace.race.distance}m ダート</div>
              <div>🌤️ {selectedRace.race.weather}</div>
              <div>🏇 馬場: {selectedRace.race.track_condition}</div>
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
                  {selectedRace.race.entries.map((entry, index) => (
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
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-yellow-50 to-orange-50 p-8">
      <button
        onClick={onBack}
        className="mb-6 px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700"
      >
        ← 戻る
      </button>

      <h1 className="text-3xl font-bold mb-2 text-yellow-600">
        {formatDate(date)} の全レース予想
      </h1>
      <p className="text-gray-600 mb-6">
        ⭐ 最高確度のレースが購入推奨です
      </p>

      {races.length === 0 ? (
        <div className="text-center py-20">
          <div className="text-4xl mb-4">📅</div>
          <div className="text-xl text-gray-600">
            この日のレースはありません
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          {races.map((raceData, index) => {
            const isTopRace = index === 0
            const prediction = raceData.prediction

            return (
              <div
                key={raceData.race.race_id}
                onClick={() => setSelectedRace(raceData)}
                className={`bg-white rounded-lg p-6 cursor-pointer transition-all ${
                  isTopRace
                    ? 'border-4 border-yellow-500 shadow-2xl'
                    : 'border-2 border-gray-300 hover:border-yellow-400 hover:shadow-lg'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    {/* レース番号 */}
                    <div
                      className={`px-4 py-2 rounded-full text-xl font-bold ${
                        isTopRace
                          ? 'bg-yellow-500 text-white'
                          : 'bg-gray-200 text-gray-700'
                      }`}
                    >
                      {raceData.race.race_number}R
                    </div>

                    {/* レース情報 */}
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="text-xl font-bold">
                          {raceData.race.name}
                        </h3>
                        {isTopRace && (
                          <span className="bg-red-500 text-white text-xs px-2 py-1 rounded-full font-bold">
                            購入推奨
                          </span>
                        )}
                      </div>
                      <div className="flex gap-4 text-sm text-gray-600">
                        <span>📏 {raceData.race.distance}m</span>
                        <span>🌤️ {raceData.race.weather}</span>
                        <span>🏇 {raceData.race.track_condition}</span>
                      </div>
                    </div>
                  </div>

                  {/* 予想と確度 */}
                  {prediction ? (
                    <div className="text-right">
                      <div className="text-sm text-gray-600 mb-1">予想</div>
                      <div className="text-2xl font-bold text-gray-800 mb-2">
                        {prediction.first} → {prediction.second} →{' '}
                        {prediction.third}
                      </div>
                      <div className="flex items-center gap-2 justify-end">
                        <span className="text-sm text-gray-600">確度</span>
                        <div
                          className={`text-3xl font-bold ${
                            isTopRace ? 'text-yellow-600' : 'text-gray-700'
                          }`}
                        >
                          {Math.round(prediction.confidence * 100)}%
                        </div>
                        {isTopRace && <span className="text-2xl">⭐</span>}
                      </div>
                    </div>
                  ) : (
                    <div className="text-gray-400">予想なし</div>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      )}

      {/* 購入ルール説明 */}
      {topRace && (
        <div className="mt-8 p-6 bg-blue-50 border-2 border-blue-300 rounded-lg">
          <h3 className="font-bold text-lg mb-2 text-blue-800">
            💡 購入ルール
          </h3>
          <ul className="text-sm text-blue-700 space-y-1">
            <li>
              • 1日に購入するのは<strong>最高確度の1レースのみ</strong>
            </li>
            <li>
              • 今日の推奨: <strong>{topRace.race.race_number}R</strong>{' '}
              {topRace.race.name} （確度{' '}
              {Math.round((topRace.prediction?.confidence || 0) * 100)}%）
            </li>
            <li>• 3連単を100円〜購入</li>
            <li>• レース後に結果を記録</li>
          </ul>
        </div>
      )}
    </div>
  )
}
