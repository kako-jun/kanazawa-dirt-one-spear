'use client'

import { Race } from '@/lib/api-client'

interface RaceListProps {
  races: Race[]
  onRaceSelect: (raceId: string) => void
  onDateSelect?: (date: string) => void
}

export default function RaceList({
  races,
  onRaceSelect,
  onDateSelect,
}: RaceListProps) {
  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr)
    return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
  }

  const getDateOnly = (dateStr: string) => {
    return dateStr.split('T')[0]
  }

  const handleRaceClick = (race: Race) => {
    onRaceSelect(race.race_id)
  }

  // グループ化：日付ごとにレースをまとめる
  const racesByDate = races.reduce((acc, race) => {
    const dateKey = getDateOnly(race.date)
    if (!acc[dateKey]) {
      acc[dateKey] = []
    }
    acc[dateKey].push(race)
    return acc
  }, {} as Record<string, Race[]>)

  // 日付順にソート
  const sortedDates = Object.keys(racesByDate).sort((a, b) => {
    return new Date(b).getTime() - new Date(a).getTime()
  })

  if (races.length === 0) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center p-8">
          <div className="text-4xl mb-4">🏇</div>
          <div className="text-xl text-gray-600">
            現在、レース情報がありません
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6 text-yellow-600">
        金沢競馬 レース一覧
      </h2>

      <div className="space-y-8">
        {sortedDates.map((dateKey) => {
          const dateRaces = racesByDate[dateKey]
          const raceCount = dateRaces.length

          return (
            <div key={dateKey} className="space-y-4">
              {/* 日付ヘッダー */}
              <div className="flex items-center justify-between bg-gradient-to-r from-yellow-600 to-orange-600 text-white p-4 rounded-lg shadow-lg">
                <div>
                  <h3 className="text-2xl font-bold">
                    {formatDate(dateKey)}
                  </h3>
                  <p className="text-sm opacity-90">全{raceCount}レース</p>
                </div>
                {onDateSelect && (
                  <button
                    onClick={() => onDateSelect(dateKey)}
                    className="px-4 py-2 bg-white text-yellow-600 rounded-lg font-bold hover:bg-yellow-50 transition-colors"
                  >
                    全レースの予想を見る →
                  </button>
                )}
              </div>

              {/* レース一覧 */}
              <div className="grid gap-3">
                {dateRaces.map((race) => (
                  <div
                    key={race.race_id}
                    onClick={() => handleRaceClick(race)}
                    className="bg-white border-2 border-gray-300 rounded-lg p-4 cursor-pointer hover:border-yellow-600 hover:shadow-lg transition-all"
                    role="button"
                    tabIndex={0}
                    aria-label={`第${race.race_number}レース ${race.name}`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <div className="bg-yellow-600 text-white px-3 py-1 rounded-full text-sm font-bold">
                            {race.race_number}R
                          </div>
                          <div className="text-lg font-bold">{race.name}</div>
                        </div>

                        <div className="flex gap-4 text-sm text-gray-600">
                          <div className="flex items-center gap-1">
                            <span>📏</span>
                            <span>{race.distance}m</span>
                          </div>
                          <div className="flex items-center gap-1">
                            <span>🌤️</span>
                            <span>{race.weather}</span>
                          </div>
                          <div className="flex items-center gap-1">
                            <span>🏇</span>
                            <span>馬場: {race.track_condition}</span>
                          </div>
                        </div>

                        <div className="mt-2 text-sm text-gray-500">
                          出走頭数: {race.entries.length}頭
                        </div>
                      </div>

                      <div className="text-yellow-600 text-2xl">→</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
