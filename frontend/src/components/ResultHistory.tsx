'use client'

import { Result, Race } from '@/lib/api-client'

interface ResultHistoryProps {
  results: Result[]
  races: Race[]
}

export default function ResultHistory({ results, races }: ResultHistoryProps) {
  const getRaceName = (raceId: string) => {
    const race = races.find((r) => r.race_id === raceId)
    return race
      ? `${race.race_number}R ${race.name}`
      : `レースID: ${raceId}`
  }

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr)
    return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:${String(
      date.getMinutes()
    ).padStart(2, '0')}`
  }

  if (results.length === 0) {
    return (
      <div className="text-center py-20">
        <div className="text-4xl mb-4">📝</div>
        <div className="text-base text-retro-brown font-serif">まだ結果が登録されていません</div>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {results.map((result) => (
        <div
          key={result.result_id}
          className="betting-slip rounded-sm p-5"
          style={{
            borderLeftColor: result.prediction_hit ? '#C8102E' : '#8B5E3C',
            background: result.prediction_hit ? 'rgba(200,16,46,0.03)' : undefined,
          }}
        >
          <div className="flex items-start justify-between mb-3">
            <div>
              <div className="font-serif font-black text-retro-brown-dark text-base">{getRaceName(result.race_id)}</div>
              <div className="text-xs text-retro-brown opacity-60 font-mono mt-1">
                {formatDate(result.recorded_at)}
              </div>
            </div>

            {/* 的中表示 */}
            {result.prediction_hit ? (
              <div className="hit-stamp w-14 h-14 flex items-center justify-center text-xs leading-tight stamp-appear">
                的中!
              </div>
            ) : (
              <div className="miss-stamp w-12 h-12 flex items-center justify-center text-xs leading-tight">
                不的中
              </div>
            )}
          </div>

          {/* 着順 — LED風 */}
          <div className="mb-3">
            <div className="text-xs text-retro-brown mb-1 font-mono opacity-70">着順</div>
            <div className="led-display inline-block rounded-sm text-xl font-black tracking-[0.3em]">
              {result.first} - {result.second} - {result.third}
            </div>
          </div>

          {/* 配当 */}
          {result.payout_trifecta && (
            <div className="mb-3">
              <div className="text-xs text-retro-brown mb-1 font-mono opacity-70">三連単配当</div>
              <div
                className="text-2xl font-black text-retro-gold font-mono"
                style={{ textShadow: '1px 1px 0 rgba(139,101,0,0.4)' }}
              >
                ¥{result.payout_trifecta.toLocaleString()}
              </div>
            </div>
          )}

          {/* 購入情報 */}
          {result.purchased && (
            <div
              className="rounded-sm p-3 mb-3"
              style={{
                background: 'rgba(44,95,138,0.08)',
                border: '1px solid rgba(44,95,138,0.2)'
              }}
            >
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <div className="text-xs text-retro-brown font-mono opacity-60">購入金額</div>
                  <div className="font-bold font-mono text-retro-brown-dark">
                    ¥{result.bet_amount?.toLocaleString()}
                  </div>
                </div>
                <div>
                  <div className="text-xs text-retro-brown font-mono opacity-60">払戻金額</div>
                  <div className="font-bold text-retro-gold font-mono">
                    ¥{result.return_amount?.toLocaleString()}
                  </div>
                </div>
                <div className="col-span-2">
                  <div className="text-xs text-retro-brown font-mono opacity-60">収支</div>
                  <div
                    className={`text-lg font-black font-mono ${
                      (result.return_amount || 0) - (result.bet_amount || 0) > 0
                        ? 'text-retro-gold'
                        : 'text-retro-crimson'
                    }`}
                  >
                    {(result.return_amount || 0) - (result.bet_amount || 0) > 0 ? '+' : ''}
                    ¥{((result.return_amount || 0) - (result.bet_amount || 0)).toLocaleString()}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* メモ */}
          {result.memo && (
            <div
              className="text-sm text-retro-brown p-3 rounded-sm font-mono"
              style={{
                background: 'rgba(0,0,0,0.04)',
                border: '1px solid rgba(139,94,60,0.2)'
              }}
            >
              <div className="text-xs opacity-60 mb-1">メモ</div>
              {result.memo}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
