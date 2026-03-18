import { Race, Prediction } from '@/lib/api-client'

interface LatestPredictionSectionProps {
  race: Race | null
  prediction: Prediction | null
}

export default function LatestPredictionSection({ race, prediction }: LatestPredictionSectionProps) {
  // データがない場合は表示しない
  if (!race || !prediction) {
    return (
      <section className="py-12 md:py-16 bg-retro-sepia">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-8">
            <h2 className="showa-section-title text-2xl md:text-3xl">
              次回レース オッズ順予想
            </h2>
          </div>
          <div className="betting-slip max-w-2xl mx-auto p-6 md:p-8 text-center text-retro-brown">
            <p>予想はまだ生成されていません</p>
            <p className="text-sm mt-2 opacity-75">レースデータが登録され次第、予想を生成します</p>
          </div>
        </div>
      </section>
    )
  }

  // 日付フォーマット
  const raceDate = new Date(race.date)
  const dateStr = `${raceDate.getFullYear()}年${raceDate.getMonth() + 1}月${raceDate.getDate()}日`
  const dayOfWeek = ['日', '月', '火', '水', '木', '金', '土'][raceDate.getDay()]

  // 予想の組み合わせ
  const predictionStr = `${prediction.first}-${prediction.second}-${prediction.third}`

  // 信頼度をパーセント表示
  const confidencePercent = Math.round(prediction.confidence * 100)

  return (
    <section className="py-12 md:py-16 bg-retro-sepia">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* セクションタイトル */}
        <div className="text-center mb-8">
          <h2 className="showa-section-title text-2xl md:text-3xl">
            次回レース オッズ順予想
          </h2>
        </div>

        {/* 馬券スタイルのカード */}
        <div className="max-w-2xl mx-auto">
          <div className="betting-slip p-6 md:p-8 rounded-sm">
            {/* 馬券ヘッダー — レース情報 */}
            <div className="text-center mb-6 pb-4 border-b-2 border-dashed border-retro-wheat-dark">
              {/* "競" スタンプ風 */}
              <div className="inline-block mb-3 px-3 py-1 text-xs font-bold font-mono tracking-widest border-2 border-retro-brown text-retro-brown opacity-70">
                金沢競馬
              </div>
              <p className="text-xl md:text-2xl font-serif font-bold text-retro-brown-dark">
                {dateStr}（{dayOfWeek}）
              </p>
              <p className="text-base md:text-lg text-retro-brown mt-1 font-bold">
                第{race.race_number}R {race.name}
              </p>
              <p className="text-sm text-retro-brown-light mt-1 font-mono">
                {race.distance}m · {race.track_condition} · {race.weather}
              </p>
            </div>

            {/* 一本槍ビジュアル */}
            <div className="flex flex-col items-center my-8">
              <div className="relative flex flex-col items-center">
                {/* 槍の穂先 */}
                <div
                  className="w-0 h-0 mb-3"
                  style={{
                    borderLeft: '18px solid transparent',
                    borderRight: '18px solid transparent',
                    borderBottom: '36px solid #3D1C0E',
                    filter: 'drop-shadow(2px 2px 2px rgba(0,0,0,0.4))'
                  }}
                />

                {/* 1着 */}
                <div className="flex flex-col items-center mb-4">
                  <div
                    className="place-badge-1 w-20 h-20 md:w-24 md:h-24 rounded flex flex-col items-center justify-center text-4xl md:text-5xl font-mono font-black"
                    style={{ borderRadius: '4px' }}
                  >
                    <span>{prediction.first}</span>
                  </div>
                  <span className="text-xs mt-2 text-retro-brown font-bold font-mono tracking-wide">
                    穂先（本命）
                  </span>
                </div>

                {/* 柄（軸） */}
                <div
                  className="w-3 h-8 bg-retro-brown-dark mb-3"
                  style={{ boxShadow: '1px 0 0 rgba(255,255,255,0.1), -1px 0 0 rgba(0,0,0,0.3)' }}
                />

                {/* 相手・穴馬 */}
                <div className="flex justify-center gap-4">
                  <div className="flex flex-col items-center">
                    <div
                      className="place-badge-2 w-14 h-14 md:w-16 md:h-16 rounded flex flex-col items-center justify-center text-2xl md:text-3xl font-mono font-black"
                      style={{ borderRadius: '4px' }}
                    >
                      {prediction.second}
                    </div>
                    <span className="text-xs mt-1 text-center text-retro-brown font-mono">相手</span>
                  </div>
                  <div className="flex flex-col items-center">
                    <div
                      className="place-badge-3 w-14 h-14 md:w-16 md:h-16 rounded flex flex-col items-center justify-center text-2xl md:text-3xl font-mono font-black"
                      style={{ borderRadius: '4px' }}
                    >
                      {prediction.third}
                    </div>
                    <span className="text-xs mt-1 text-center text-retro-brown font-mono">穴馬</span>
                  </div>
                </div>

                {/* 柄の下部 */}
                <div
                  className="mx-auto mt-2"
                  style={{
                    width: '10px',
                    height: '60px',
                    background: 'linear-gradient(180deg, #3D1C0E 0%, #5A2D1A 60%, #4A2018 100%)',
                    boxShadow: '2px 0 0 rgba(255,255,255,0.1), -1px 0 0 rgba(0,0,0,0.4)',
                    borderRadius: '0 0 3px 3px'
                  }}
                />
              </div>
            </div>

            {/* LED電光掲示板 — 三連単予想 */}
            <div className="led-display text-center mb-6 rounded-sm">
              <div className="text-xs mb-2 opacity-70 tracking-widest">三連単予想</div>
              <div className="text-3xl md:text-4xl font-bold tracking-[0.5em] led-flicker">
                {predictionStr}
              </div>
            </div>

            {/* 信頼度 */}
            <div className="text-center mb-6">
              <div className="text-sm text-retro-brown mb-2 font-bold">信頼度</div>
              <div className="flex items-center justify-center gap-2">
                <div className="flex gap-1">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <span
                      key={star}
                      className={`text-2xl ${
                        star <= Math.floor(confidencePercent / 20)
                          ? 'text-retro-gold'
                          : 'text-retro-wheat-dark'
                      }`}
                      style={star <= Math.floor(confidencePercent / 20) ? {
                        textShadow: '0 0 4px rgba(201,146,10,0.5)'
                      } : {}}
                    >
                      ★
                    </span>
                  ))}
                </div>
                <span className="text-2xl font-black text-retro-crimson font-mono"
                  style={{ textShadow: '1px 1px 0 rgba(139,0,0,0.5)' }}>
                  {confidencePercent}%
                </span>
              </div>
            </div>

            {/* 予想根拠 */}
            <div className="border-t-2 border-dashed border-retro-wheat-dark pt-6">
              <h3 className="font-bold text-retro-brown mb-3 text-center text-sm tracking-wide">
                — 予想根拠 —
              </h3>
              <div className="space-y-2">
                <p className="text-sm md:text-base font-mono">
                  <span className="text-retro-crimson font-bold">✓</span>{' '}
                  モデルバージョン: {prediction.model_version}
                </p>
                <p className="text-sm md:text-base font-mono">
                  <span className="text-retro-crimson font-bold">✓</span>{' '}
                  過去のレースデータから算出
                </p>
                <p className="text-sm md:text-base font-mono">
                  <span className="text-retro-crimson font-bold">✓</span>{' '}
                  馬場状態「{race.track_condition}」を考慮
                </p>
              </div>
            </div>

            {/* アクションボタン */}
            <div className="mt-6 flex flex-col sm:flex-row gap-3 justify-center">
              <a
                href="/ai"
                className="px-6 py-3 bg-retro-blue text-white rounded font-bold text-center hover:bg-retro-blue-light transition-colors border-2 border-retro-blue text-sm"
                style={{ boxShadow: '2px 2px 0 rgba(0,0,0,0.3)' }}
              >
                詳細を見る
              </a>
              <a
                href="/ai"
                className="px-6 py-3 bg-retro-green text-white rounded font-bold text-center hover:bg-opacity-90 transition-colors border-2 border-retro-green text-sm"
                style={{ boxShadow: '2px 2px 0 rgba(0,0,0,0.3)' }}
              >
                買い目シミュレーション
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
