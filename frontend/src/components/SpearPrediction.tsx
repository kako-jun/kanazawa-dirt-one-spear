'use client'

import { Prediction, Entry } from '@/lib/api-client'

interface SpearPredictionProps {
  prediction: Prediction
  entries: Entry[]
}

export default function SpearPrediction({
  prediction,
  entries,
}: SpearPredictionProps) {
  const getHorseInfo = (horseNumber: number) => {
    return entries.find((e) => e.horse_number === horseNumber)
  }

  const first = getHorseInfo(prediction.first)
  const second = getHorseInfo(prediction.second)
  const third = getHorseInfo(prediction.third)

  return (
    <div
      className="flex flex-col items-center justify-center p-8"
      aria-label={`一本槍予想 3連単 ${prediction.first}-${prediction.second}-${prediction.third}`}
    >
      {/* タイトル */}
      <h2 className="text-3xl font-bold mb-8 text-yellow-600">
        ⚔️ 一本槍予想 ⚔️
      </h2>

      {/* 槍と団子のビジュアル */}
      <div className="relative flex flex-col items-center">
        {/* 槍の穂先 */}
        <div className="w-0 h-0 border-l-[30px] border-l-transparent border-r-[30px] border-r-transparent border-b-[60px] border-b-gray-700 mb-4"></div>

        {/* 1着（一番上の団子） */}
        <div className="relative mb-4">
          <div className="w-32 h-32 rounded-full bg-gradient-to-br from-yellow-400 to-yellow-600 shadow-2xl flex flex-col items-center justify-center border-4 border-yellow-700">
            <div className="text-4xl font-bold text-white">
              {prediction.first}
            </div>
            <div className="text-xs text-white mt-1">1着</div>
          </div>
          {first && (
            <div className="absolute -right-48 top-1/2 -translate-y-1/2 text-left bg-white/90 p-3 rounded-lg shadow-lg border-2 border-yellow-600 min-w-[160px]">
              <div className="font-bold text-lg">{first.horse.name}</div>
              <div className="text-sm text-gray-600">{first.jockey}</div>
            </div>
          )}
        </div>

        {/* 2着（真ん中の団子） */}
        <div className="relative mb-4">
          <div className="w-32 h-32 rounded-full bg-gradient-to-br from-gray-300 to-gray-500 shadow-2xl flex flex-col items-center justify-center border-4 border-gray-600">
            <div className="text-4xl font-bold text-white">
              {prediction.second}
            </div>
            <div className="text-xs text-white mt-1">2着</div>
          </div>
          {second && (
            <div className="absolute -right-48 top-1/2 -translate-y-1/2 text-left bg-white/90 p-3 rounded-lg shadow-lg border-2 border-gray-500 min-w-[160px]">
              <div className="font-bold text-lg">{second.horse.name}</div>
              <div className="text-sm text-gray-600">{second.jockey}</div>
            </div>
          )}
        </div>

        {/* 3着（一番下の団子） */}
        <div className="relative mb-4">
          <div className="w-32 h-32 rounded-full bg-gradient-to-br from-orange-400 to-orange-600 shadow-2xl flex flex-col items-center justify-center border-4 border-orange-700">
            <div className="text-4xl font-bold text-white">
              {prediction.third}
            </div>
            <div className="text-xs text-white mt-1">3着</div>
          </div>
          {third && (
            <div className="absolute -right-48 top-1/2 -translate-y-1/2 text-left bg-white/90 p-3 rounded-lg shadow-lg border-2 border-orange-600 min-w-[160px]">
              <div className="font-bold text-lg">{third.horse.name}</div>
              <div className="text-sm text-gray-600">{third.jockey}</div>
            </div>
          )}
        </div>

        {/* 槍の柄 */}
        <div className="w-4 h-64 bg-gradient-to-b from-gray-700 to-gray-900 rounded-b-lg"></div>
      </div>

      {/* 信頼度表示 */}
      <div className="mt-8 text-center">
        <div className="text-sm text-gray-600">信頼度</div>
        <div className="text-2xl font-bold text-yellow-600">
          {Math.round(prediction.confidence * 100)}%
        </div>
      </div>

      {/* 券種表示 */}
      <div className="mt-6 p-4 bg-yellow-100 rounded-lg border-2 border-yellow-600">
        <div className="text-center">
          <div className="text-sm text-gray-600">3連単</div>
          <div className="text-3xl font-bold text-gray-800">
            {prediction.first} → {prediction.second} → {prediction.third}
          </div>
        </div>
      </div>

      {/* 注意書き */}
      <div className="mt-8 text-xs text-gray-500 text-center max-w-md">
        ※趣味・無料・応援目的の予想です。必ず当たるものではありません。
        <br />
        ※ギャンブルは適度に楽しみましょう。
      </div>
    </div>
  )
}
