export default function RacecourseSection() {
  const places = [
    {
      title: 'レトロな食堂',
      description: '昭和の香り漂う競馬場の食堂。メニューはカツカレー¥500、ラーメン¥400など、庶民的な価格。ボロボロだけど、それがいい。',
      features: ['カツカレー ¥500', 'ラーメン ¥400', '昭和レトロな雰囲気'],
      icon: '🍛',
    },
    {
      title: '中央公園へ続くトンネル',
      description: 'スタンドから中央公園へ続く薄暗いトンネル。レース前の静寂、期待と緊張。馬券を握りしめて歩く道。',
      features: ['薄暗い独特の雰囲気', 'レース前の緊張感', '競馬場の裏側'],
      icon: '🚶',
    },
    {
      title: '中央公園の憩い',
      description: 'トンネルを抜けると広がる緑豊かな公園。家族連れで賑わい、子供が遊び、大人は馬券を研究。競馬場のもう一つの顔。',
      features: ['緑豊かな広場', '家族連れで楽しめる', 'ピクニック気分'],
      icon: '🌳',
    },
  ]

  return (
    <section className="py-12 md:py-16 bg-retro-sepia">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* セクションタイトル */}
        <div className="text-center mb-4">
          <h2 className="showa-section-title text-2xl md:text-3xl">
            金沢競馬場のいいところ
          </h2>
        </div>
        <p className="text-center text-retro-brown opacity-75 mb-8 text-sm font-mono">
          — 昭和レトロな雰囲気が残る、温かみのある競馬場 —
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {places.map((place, index) => (
            <div
              key={index}
              className="aged-paper-card p-6 rounded-sm hover:shadow-retro-lg transition-shadow"
            >
              {/* 画像プレースホルダー — ダートっぽい質感 */}
              <div
                className="horse-silhouette-placeholder border-2 border-retro-brown h-40 rounded-sm mb-4 flex items-center justify-center relative"
              >
                <div className="text-center relative z-10">
                  <div className="text-4xl mb-1">{place.icon}</div>
                  <div className="text-xs text-retro-wheat opacity-70 font-mono">写真準備中</div>
                </div>
              </div>

              {/* タイトル */}
              <h3 className="text-lg font-serif font-black text-retro-brown-dark mb-2 leading-snug"
                style={{ textShadow: '1px 1px 0 rgba(0,0,0,0.1)' }}>
                {place.title}
              </h3>

              {/* 説明 */}
              <p className="text-sm text-retro-brown mb-4 leading-relaxed">
                {place.description}
              </p>

              {/* 特徴リスト */}
              <div className="space-y-1 border-t border-dashed border-retro-wheat-dark pt-3">
                {place.features.map((feature, fIndex) => (
                  <div
                    key={fIndex}
                    className="flex items-center gap-2 text-sm"
                  >
                    <span className="text-retro-crimson font-bold">◆</span>
                    <span className="text-retro-brown font-mono text-xs">{feature}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* 競馬場ページへのリンク */}
        <div className="text-center mb-12">
          <a
            href="/racecourse"
            className="inline-block px-8 py-4 font-bold text-lg rounded text-white border-2 border-retro-green"
            style={{
              background: 'linear-gradient(180deg, #2E6B2E 0%, #1E4A1E 100%)',
              boxShadow: '4px 4px 0 rgba(0,0,0,0.3)',
              textShadow: '1px 1px 2px rgba(0,0,0,0.5)'
            }}
          >
            もっと詳しく見る
          </a>
        </div>

        {/* 応援メッセージ — 看板スタイル */}
        <div className="showa-sign p-6 md:p-8 text-center rounded-sm">
          <h3
            className="text-2xl font-serif font-black text-retro-gold mb-4"
            style={{ textShadow: '2px 2px 4px rgba(0,0,0,0.7), 0 0 8px rgba(201,146,10,0.3)' }}
          >
            金沢競馬を応援しよう
          </h3>
          <p className="text-retro-wheat mb-4 leading-relaxed opacity-90">
            地方競馬は全国で廃止が相次いでいます。
            <br className="hidden sm:inline" />
            金沢競馬場を未来に残すため、馬券購入で応援しましょう。
          </p>
          <p className="text-xs text-retro-wheat opacity-60 font-mono">
            ※ 全国どこからでも楽天競馬などのオンラインサービスで購入できます
          </p>
        </div>
      </div>
    </section>
  )
}
