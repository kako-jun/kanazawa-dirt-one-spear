export default function RacecourseSection() {
  const places = [
    {
      title: 'レトロな食堂',
      description: '昭和の香り漂う競馬場の食堂。メニューはカツカレー¥500、ラーメン¥400など、庶民的な価格。ボロボロだけど、それがいい。',
      features: ['カツカレー ¥500', 'ラーメン ¥400', '昭和レトロな雰囲気'],
    },
    {
      title: '中央公園へ続くトンネル',
      description: 'スタンドから中央公園へ続く薄暗いトンネル。レース前の静寂、期待と緊張。馬券を握りしめて歩く道。',
      features: ['薄暗い独特の雰囲気', 'レース前の緊張感', '競馬場の裏側'],
    },
    {
      title: '中央公園の憩い',
      description: 'トンネルを抜けると広がる緑豊かな公園。家族連れで賑わい、子供が遊び、大人は馬券を研究。競馬場のもう一つの顔。',
      features: ['緑豊かな広場', '家族連れで楽しめる', 'ピクニック気分'],
    },
  ]

  return (
    <section className="py-12 md:py-16 bg-retro-sepia">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl md:text-4xl font-serif font-bold text-retro-brown text-center mb-4">
          金沢競馬場のいいところ
        </h2>
        <p className="text-center text-retro-dark-gray mb-8">
          昭和レトロな雰囲気が残る、温かみのある競馬場
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {places.map((place, index) => (
            <div
              key={index}
              className="newspaper-card p-6 hover:shadow-xl transition-shadow"
            >
              {/* 画像プレースホルダー */}
              <div className="bg-retro-wheat border-2 border-retro-brown h-48 rounded-lg mb-4 flex items-center justify-center">
                <div className="text-retro-brown text-center">
                  <div className="text-4xl mb-2">
                    {index === 0 ? '🍛' : index === 1 ? '🚶' : '🌳'}
                  </div>
                  <div className="text-sm opacity-75">写真準備中</div>
                </div>
              </div>

              {/* タイトル */}
              <h3 className="text-xl font-serif font-bold text-retro-brown mb-3">
                {place.title}
              </h3>

              {/* 説明 */}
              <p className="text-sm text-retro-dark-gray mb-4 leading-relaxed">
                {place.description}
              </p>

              {/* 特徴 */}
              <div className="space-y-1">
                {place.features.map((feature, fIndex) => (
                  <div
                    key={fIndex}
                    className="flex items-start gap-2 text-sm"
                  >
                    <span className="text-retro-green font-bold">✓</span>
                    <span className="text-retro-brown">{feature}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* 競馬場ページへのリンク */}
        <div className="text-center">
          <a
            href="/racecourse"
            className="inline-block px-8 py-4 bg-retro-green text-white rounded-lg font-bold text-lg hover:bg-opacity-90 transition-colors shadow-retro"
          >
            もっと詳しく見る
          </a>
        </div>

        {/* 応援メッセージ */}
        <div className="mt-12 newspaper-card p-6 md:p-8 text-center">
          <h3 className="text-2xl font-serif font-bold text-retro-crimson mb-4">
            金沢競馬を応援しよう
          </h3>
          <p className="text-retro-dark-gray mb-4 leading-relaxed">
            地方競馬は全国で廃止が相次いでいます。
            <br className="hidden sm:inline" />
            金沢競馬場を未来に残すため、馬券購入で応援しましょう。
          </p>
          <p className="text-sm text-retro-brown">
            ※ 全国どこからでも楽天競馬などのオンラインサービスで購入できます
          </p>
        </div>
      </div>
    </section>
  )
}
