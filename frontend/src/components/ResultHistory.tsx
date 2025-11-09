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
        <div className="text-xl text-gray-600">まだ結果が登録されていません</div>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {results.map((result) => (
        <div
          key={result.result_id}
          className={`bg-white border-2 rounded-lg p-5 ${
            result.prediction_hit
              ? 'border-yellow-500 bg-yellow-50'
              : 'border-gray-300'
          }`}
        >
          <div className="flex items-start justify-between mb-3">
            <div>
              <div className="font-bold text-lg">{getRaceName(result.race_id)}</div>
              <div className="text-sm text-gray-500">
                {formatDate(result.recorded_at)}
              </div>
            </div>

            {/* 的中表示 */}
            <div
              className={`px-4 py-2 rounded-full font-bold text-lg ${
                result.prediction_hit
                  ? 'bg-yellow-500 text-white'
                  : 'bg-gray-300 text-gray-700'
              }`}
            >
              {result.prediction_hit ? '◯ 的中！' : '× 不的中'}
            </div>
          </div>

          {/* 着順 */}
          <div className="mb-3">
            <div className="text-sm text-gray-600 mb-1">着順</div>
            <div className="text-2xl font-bold">
              {result.first} → {result.second} → {result.third}
            </div>
          </div>

          {/* 配当 */}
          {result.payout_trifecta && (
            <div className="mb-3">
              <div className="text-sm text-gray-600 mb-1">3連単配当</div>
              <div className="text-xl font-bold text-orange-600">
                ¥{result.payout_trifecta.toLocaleString()}
              </div>
            </div>
          )}

          {/* 購入情報 */}
          {result.purchased && (
            <div className="bg-blue-50 border border-blue-200 rounded p-3 mb-3">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <div className="text-xs text-gray-600">購入金額</div>
                  <div className="font-bold">
                    ¥{result.bet_amount?.toLocaleString()}
                  </div>
                </div>
                <div>
                  <div className="text-xs text-gray-600">払戻金額</div>
                  <div className="font-bold text-green-600">
                    ¥{result.return_amount?.toLocaleString()}
                  </div>
                </div>
                <div className="col-span-2">
                  <div className="text-xs text-gray-600">収支</div>
                  <div
                    className={`text-lg font-bold ${
                      (result.return_amount || 0) - (result.bet_amount || 0) > 0
                        ? 'text-green-600'
                        : 'text-red-600'
                    }`}
                  >
                    {(result.return_amount || 0) - (result.bet_amount || 0) > 0
                      ? '+'
                      : ''}
                    ¥
                    {(
                      (result.return_amount || 0) - (result.bet_amount || 0)
                    ).toLocaleString()}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* メモ */}
          {result.memo && (
            <div className="text-sm text-gray-700 bg-gray-50 p-3 rounded">
              <div className="text-xs text-gray-500 mb-1">メモ</div>
              {result.memo}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
