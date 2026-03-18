export default function HeroSection() {
  return (
    <section className="relative bg-retro-slate text-retro-sepia py-12 md:py-20 overflow-hidden">
      {/* ダートコーステクスチャ — ニュアンスを出す背景オーバーレイ */}
      <div className="absolute inset-0 opacity-20"
        style={{
          backgroundImage: `
            radial-gradient(ellipse at 15% 50%, rgba(155,101,67,0.6) 0%, transparent 60%),
            radial-gradient(ellipse at 85% 60%, rgba(107,58,42,0.4) 0%, transparent 50%),
            repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(107,58,42,0.05) 10px, rgba(107,58,42,0.05) 11px)
          `
        }}
      />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          {/* メインキャッチコピー — 昭和看板スタイル */}
          <div className="relative inline-block mb-8 w-full max-w-2xl mx-auto">
            {/* 看板枠の上のデコレーション */}
            <div className="flex items-center justify-center gap-3 mb-2 opacity-60">
              <div className="h-px flex-1 bg-retro-gold-dark" />
              <span className="text-retro-gold text-xs font-mono tracking-widest">◆◆◆</span>
              <div className="h-px flex-1 bg-retro-gold-dark" />
            </div>

            {/* 看板本体 */}
            <div className="showa-sign py-6 px-8 text-center">
              <h2 className="text-2xl md:text-4xl font-serif font-black text-retro-wheat leading-relaxed tracking-wide"
                style={{ textShadow: '2px 2px 4px rgba(0,0,0,0.7)' }}>
                三連単、一点勝負
              </h2>
              <p className="text-xl md:text-3xl font-serif font-bold text-retro-gold mt-2"
                style={{ textShadow: '1px 1px 3px rgba(0,0,0,0.6), 0 0 8px rgba(201,146,10,0.3)' }}>
                データが選ぶ、本命の一本槍
              </p>
            </div>

            {/* 看板枠の下のデコレーション */}
            <div className="flex items-center justify-center gap-3 mt-2 opacity-60">
              <div className="h-px flex-1 bg-retro-gold-dark" />
              <span className="text-retro-gold text-xs font-mono tracking-widest">◆◆◆</span>
              <div className="h-px flex-1 bg-retro-gold-dark" />
            </div>
          </div>

          {/* サブテキスト */}
          <div className="max-w-2xl mx-auto space-y-3 mb-8">
            <p className="text-base md:text-lg leading-relaxed opacity-90">
              金沢競馬に特化したデータ分析予想システム。
              <br className="hidden sm:inline" />
              膨大なデータから導き出す、三連単の一点予想。
            </p>
            <p className="text-sm opacity-70 font-mono tracking-wide">
              — 趣味・無料・応援目的のプロジェクト —
            </p>
          </div>

          {/* アクションボタン */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <a
              href="/ai"
              className="retro-button px-8 py-4 rounded text-lg font-black inline-block min-w-[200px]"
            >
              最新のオッズ順予想を見る
            </a>
            <a
              href="/stats"
              className="px-8 py-4 bg-transparent text-retro-wheat rounded text-lg font-bold border-2 border-retro-wheat hover:bg-retro-wheat hover:text-retro-brown transition-colors min-w-[200px] text-center"
              style={{ boxShadow: '3px 3px 0 rgba(0,0,0,0.3)' }}
            >
              統計・的中実績
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}
