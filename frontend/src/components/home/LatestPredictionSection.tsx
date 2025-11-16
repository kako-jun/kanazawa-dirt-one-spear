export default function LatestPredictionSection() {
  // TODO: 実際のデータはAPIから取得
  const latestPrediction = {
    date: '2025年11月16日（土）',
    race: '第3R',
    prediction: '7-3-5',
    confidence: 82,
    reasoning: [
      '7番は過去5走平均2.1着',
      '馬場「良」で勝率40%',
      '中島騎手との相性◎',
    ],
  }

  return (
    <section className="py-12 md:py-16 bg-retro-sepia">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl md:text-4xl font-serif font-bold text-retro-brown text-center mb-8">
          次回レース AI予想
        </h2>

        <div className="newspaper-card max-w-2xl mx-auto p-6 md:p-8">
          {/* レース情報 */}
          <div className="text-center mb-6">
            <p className="text-lg md:text-xl font-bold text-retro-dark-gray">
              {latestPrediction.date}
            </p>
            <p className="text-base md:text-lg text-retro-brown mt-1">
              {latestPrediction.race}
            </p>
          </div>

          {/* 一本槍ビジュアル */}
          <div className="flex flex-col items-center my-8">
            <div className="relative">
              {/* 穂先（本命） */}
              <div className="flex flex-col items-center">
                <div className="w-16 h-16 md:w-20 md:h-20 bg-retro-crimson text-white rounded-lg flex items-center justify-center text-3xl md:text-4xl font-mono font-bold shadow-retro">
                  {latestPrediction.prediction.split('-')[0]}
                </div>
                <span className="text-sm mt-2 text-retro-brown font-bold">
                  穂先（本命）
                </span>
              </div>

              {/* 団子（相手） */}
              <div className="flex justify-center gap-4 mt-4">
                <div>
                  <div className="w-12 h-12 md:w-16 md:h-16 bg-retro-brown text-white rounded-full flex items-center justify-center text-xl md:text-2xl font-mono font-bold">
                    {latestPrediction.prediction.split('-')[1]}
                  </div>
                  <span className="text-xs mt-1 block text-center">相手</span>
                </div>
                <div>
                  <div className="w-12 h-12 md:w-16 md:h-16 bg-retro-brown text-white rounded-full flex items-center justify-center text-xl md:text-2xl font-mono font-bold">
                    {latestPrediction.prediction.split('-')[2]}
                  </div>
                  <span className="text-xs mt-1 block text-center">穴馬</span>
                </div>
              </div>

              {/* 柄 */}
              <div className="mx-auto w-2 h-16 bg-retro-brown mt-2"></div>
            </div>
          </div>

          {/* 予想表示 */}
          <div className="led-display text-center mb-6">
            <div className="text-sm mb-2">三連単予想</div>
            <div className="text-2xl md:text-3xl font-bold tracking-wider">
              {latestPrediction.prediction}
            </div>
          </div>

          {/* 信頼度 */}
          <div className="text-center mb-6">
            <div className="text-sm text-retro-brown mb-2">信頼度</div>
            <div className="flex items-center justify-center gap-2">
              <div className="flex gap-1">
                {[1, 2, 3, 4, 5].map((star) => (
                  <span
                    key={star}
                    className={`text-2xl ${
                      star <= Math.floor(latestPrediction.confidence / 20)
                        ? 'text-retro-gold'
                        : 'text-gray-300'
                    }`}
                  >
                    ★
                  </span>
                ))}
              </div>
              <span className="text-xl font-bold text-retro-crimson">
                {latestPrediction.confidence}%
              </span>
            </div>
          </div>

          {/* 予想根拠 */}
          <div className="border-t-2 border-retro-brown pt-6">
            <h3 className="font-bold text-retro-brown mb-3 text-center">
              予想根拠
            </h3>
            <ul className="space-y-2">
              {latestPrediction.reasoning.map((reason, index) => (
                <li
                  key={index}
                  className="flex items-start gap-2 text-sm md:text-base"
                >
                  <span className="text-retro-crimson font-bold">✓</span>
                  <span>{reason}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* アクションボタン */}
          <div className="mt-6 flex flex-col sm:flex-row gap-3 justify-center">
            <a
              href="/ai"
              className="px-6 py-3 bg-retro-blue text-white rounded-lg font-bold text-center hover:bg-opacity-90 transition-colors"
            >
              詳細を見る
            </a>
            <a
              href="/ai"
              className="px-6 py-3 bg-retro-green text-white rounded-lg font-bold text-center hover:bg-opacity-90 transition-colors"
            >
              買い目シミュレーション
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}
