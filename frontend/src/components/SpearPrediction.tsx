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
  const confidencePercent = Math.round(prediction.confidence * 100)

  return (
    <div
      className="flex flex-col items-center justify-center p-8"
      aria-label={`一本槍予想 3連単 ${prediction.first}-${prediction.second}-${prediction.third}`}
    >
      {/* タイトル看板 */}
      <div className="showa-sign px-8 py-3 mb-8 rounded-sm inline-block">
        <h2
          className="text-2xl font-serif font-black text-retro-wheat tracking-wide text-center"
          style={{ textShadow: '2px 2px 4px rgba(0,0,0,0.7)' }}
        >
          ⚔ 一本槍予想 ⚔
        </h2>
      </div>

      {/* 槍と団子のビジュアル */}
      <div className="relative flex flex-col items-center mb-8">
        {/* 槍の穂先 */}
        <div
          className="w-0 h-0 mb-3"
          style={{
            borderLeft: '22px solid transparent',
            borderRight: '22px solid transparent',
            borderBottom: '44px solid #3D1C0E',
            filter: 'drop-shadow(2px 2px 3px rgba(0,0,0,0.5))'
          }}
        />

        {/* 1着（本命） */}
        <div className="relative mb-4">
          <div
            className="place-badge-1 w-28 h-28 md:w-32 md:h-32 flex flex-col items-center justify-center"
            style={{ borderRadius: '6px' }}
          >
            <div className="text-4xl md:text-5xl font-black font-mono text-white">
              {prediction.first}
            </div>
            <div className="text-xs text-white mt-1 opacity-80 font-mono">1着</div>
          </div>
          {first && (
            <div
              className="absolute -right-[200px] top-1/2 -translate-y-1/2 text-left p-3 min-w-[170px] rounded-sm"
              style={{
                background: '#EDE0C4',
                border: '2px solid #8B5E3C',
                boxShadow: '2px 2px 0 rgba(0,0,0,0.2)'
              }}
            >
              <div className="font-serif font-black text-retro-brown-dark text-base leading-tight">{first.horse.name}</div>
              <div className="text-xs text-retro-brown mt-1 font-mono">{first.jockey}</div>
            </div>
          )}
        </div>

        {/* 柄（軸） */}
        <div
          style={{
            width: '10px',
            height: '30px',
            background: 'linear-gradient(180deg, #3D1C0E 0%, #5A2D1A 100%)',
            boxShadow: '1px 0 0 rgba(255,255,255,0.1)'
          }}
        />

        {/* 2着 */}
        <div className="relative mb-2">
          <div
            className="place-badge-2 w-28 h-28 md:w-32 md:h-32 flex flex-col items-center justify-center"
            style={{ borderRadius: '6px' }}
          >
            <div className="text-4xl md:text-5xl font-black font-mono">
              {prediction.second}
            </div>
            <div className="text-xs mt-1 opacity-70 font-mono">2着</div>
          </div>
          {second && (
            <div
              className="absolute -right-[200px] top-1/2 -translate-y-1/2 text-left p-3 min-w-[170px] rounded-sm"
              style={{
                background: '#EDE0C4',
                border: '2px solid #8B5E3C',
                boxShadow: '2px 2px 0 rgba(0,0,0,0.2)'
              }}
            >
              <div className="font-serif font-black text-retro-brown-dark text-base leading-tight">{second.horse.name}</div>
              <div className="text-xs text-retro-brown mt-1 font-mono">{second.jockey}</div>
            </div>
          )}
        </div>

        {/* 3着 */}
        <div className="relative mb-2">
          <div
            className="place-badge-3 w-28 h-28 md:w-32 md:h-32 flex flex-col items-center justify-center"
            style={{ borderRadius: '6px' }}
          >
            <div className="text-4xl md:text-5xl font-black font-mono text-white">
              {prediction.third}
            </div>
            <div className="text-xs text-white mt-1 opacity-80 font-mono">3着</div>
          </div>
          {third && (
            <div
              className="absolute -right-[200px] top-1/2 -translate-y-1/2 text-left p-3 min-w-[170px] rounded-sm"
              style={{
                background: '#EDE0C4',
                border: '2px solid #8B5E3C',
                boxShadow: '2px 2px 0 rgba(0,0,0,0.2)'
              }}
            >
              <div className="font-serif font-black text-retro-brown-dark text-base leading-tight">{third.horse.name}</div>
              <div className="text-xs text-retro-brown mt-1 font-mono">{third.jockey}</div>
            </div>
          )}
        </div>

        {/* 槍の柄の下部 */}
        <div
          style={{
            width: '10px',
            height: '80px',
            background: 'linear-gradient(180deg, #5A2D1A 0%, #3D1C0E 60%, #2A1008 100%)',
            boxShadow: '2px 0 0 rgba(255,255,255,0.08), -1px 0 0 rgba(0,0,0,0.4)',
            borderRadius: '0 0 4px 4px'
          }}
        />
      </div>

      {/* 信頼度表示 */}
      <div className="text-center mb-6">
        <div className="text-sm text-retro-brown mb-2 font-bold font-mono">信頼度</div>
        <div
          className="text-3xl font-black text-retro-gold font-mono"
          style={{ textShadow: '1px 1px 0 rgba(139,101,0,0.5)' }}
        >
          {confidencePercent}%
        </div>
      </div>

      {/* LED掲示板 — 券種表示 */}
      <div className="led-display w-full max-w-sm rounded-sm mb-8">
        <div className="text-center">
          <div className="text-xs opacity-60 mb-2 tracking-widest">三連単</div>
          <div className="text-3xl md:text-4xl font-black tracking-[0.4em] led-flicker">
            {prediction.first} → {prediction.second} → {prediction.third}
          </div>
        </div>
      </div>

      {/* 注意書き */}
      <div className="text-xs text-retro-brown opacity-60 text-center max-w-md font-mono leading-relaxed">
        ※趣味・無料・応援目的の予想です。必ず当たるものではありません。<br />
        ※ギャンブルは適度に楽しみましょう。
      </div>
    </div>
  )
}
