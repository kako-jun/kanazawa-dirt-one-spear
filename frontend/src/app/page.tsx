import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'
import HeroSection from '@/components/home/HeroSection'
import LatestPredictionSection from '@/components/home/LatestPredictionSection'
import RecentHitsSection from '@/components/home/RecentHitsSection'
import StatsHighlightSection from '@/components/home/StatsHighlightSection'

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* ヘッダー */}
      <Header />

      {/* メインコンテンツ */}
      <main className="flex-1">
        {/* メインビジュアル */}
        <HeroSection />

        {/* 最新AI予想 */}
        <LatestPredictionSection />

        {/* 最近の的中実績 */}
        <RecentHitsSection />

        {/* 統計ハイライト */}
        <StatsHighlightSection />

        {/* 金沢競馬場の魅力セクション（後で追加） */}
        <section className="py-12 md:py-16 bg-retro-sepia">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl md:text-4xl font-serif font-bold text-retro-brown text-center mb-8">
              金沢競馬場のいいところ
            </h2>
            <div className="text-center text-retro-dark-gray">
              <p className="text-lg mb-4">
                昭和の香り漂う食堂、トンネル、中央公園...
              </p>
              <p className="mb-6">
                レトロな競馬場の魅力を写真で紹介予定
              </p>
              <a
                href="/racecourse"
                className="inline-block px-8 py-4 bg-retro-green text-white rounded-lg font-bold hover:bg-opacity-90 transition-colors"
              >
                競馬場ページへ
              </a>
            </div>
          </div>
        </section>
      </main>

      {/* フッター */}
      <Footer />
    </div>
  )
}
