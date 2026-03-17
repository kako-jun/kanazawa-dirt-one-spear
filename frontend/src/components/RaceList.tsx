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

  const sortedDates = Object.keys(racesByDate).sort((a, b) => {
    return new Date(b).getTime() - new Date(a).getTime()
  })

  if (races.length === 0) {
    return (
      <div className="flex items-center justify-center h-full bg-retro-sepia">
        <div className="text-center p-8">
          <div className="text-4xl mb-4">🏇</div>
          <div className="text-base text-retro-brown font-serif">
            現在、レース情報がありません
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6 bg-retro-sepia min-h-full">
      {/* タイトル看板 */}
      <div className="mb-6">
        <h2 className="showa-section-title text-xl">
          金沢競馬 レース一覧
        </h2>
      </div>

      <div className="space-y-8">
        {sortedDates.map((dateKey) => {
          const dateRaces = racesByDate[dateKey]
          const raceCount = dateRaces.length

          return (
            <div key={dateKey} className="space-y-3">
              {/* 日付ヘッダー — 昭和看板風 */}
              <div
                className="flex items-center justify-between p-4 rounded-sm"
                style={{
                  background: 'linear-gradient(180deg, #3D1C0E 0%, #5A2D1A 100%)',
                  border: '3px solid #2A1008',
                  borderBottom: '5px solid #1A0A04',
                  boxShadow: '4px 4px 0 rgba(0,0,0,0.4)'
                }}
              >
                <div>
                  <h3
                    className="text-xl md:text-2xl font-serif font-black text-retro-wheat"
                    style={{ textShadow: '2px 2px 4px rgba(0,0,0,0.7)' }}
                  >
                    {formatDate(dateKey)}
                  </h3>
                  <p className="text-xs text-retro-wheat opacity-60 font-mono mt-1">
                    全{raceCount}レース
                  </p>
                </div>
                {onDateSelect && (
                  <button
                    onClick={() => onDateSelect(dateKey)}
                    className="px-4 py-2 font-bold text-sm rounded text-retro-brown border-2 border-retro-wheat-dark font-mono"
                    style={{
                      background: '#E8C99A',
                      boxShadow: '2px 2px 0 rgba(0,0,0,0.3)'
                    }}
                  >
                    全予想を見る →
                  </button>
                )}
              </div>

              {/* レース一覧 */}
              <div className="grid gap-2">
                {dateRaces.map((race) => (
                  <div
                    key={race.race_id}
                    onClick={() => handleRaceClick(race)}
                    className="aged-paper-card p-4 cursor-pointer hover:shadow-retro transition-shadow rounded-sm group"
                    role="button"
                    tabIndex={0}
                    aria-label={`第${race.race_number}レース ${race.name}`}
                    onKeyDown={(e) => e.key === 'Enter' && handleRaceClick(race)}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <span className="horse-number-badge w-8 h-8 text-sm">
                            {race.race_number}
                          </span>
                          <div className="text-base font-serif font-black text-retro-brown-dark">
                            {race.name}
                          </div>
                        </div>

                        <div className="flex flex-wrap gap-3 text-xs text-retro-brown font-mono opacity-70">
                          <span>{race.distance}m</span>
                          <span>天候: {race.weather}</span>
                          <span>馬場: {race.track_condition}</span>
                          <span>{race.entries.length}頭</span>
                        </div>
                      </div>

                      <div
                        className="text-retro-gold font-bold text-xl ml-3 group-hover:translate-x-1 transition-transform"
                        style={{ textShadow: '1px 1px 0 rgba(139,101,0,0.5)' }}
                      >
                        →
                      </div>
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
