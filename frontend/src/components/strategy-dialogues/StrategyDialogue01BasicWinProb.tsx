// 作戦1: 王道・勝率予測型 (basic-win-prob)

export default function StrategyDialogue01BasicWinProb() {
  return (
    <div className="newspaper-card p-6 mb-8 bg-gradient-to-br from-retro-wheat to-white">
      <h2 className="text-2xl font-serif font-bold text-retro-brown mb-4">
        🎯 作戦1「王道・勝率予測型」
      </h2>

      <div className="space-y-4">
        {/* アヤメの発言 */}
        <div className="flex gap-3">
          <div className="flex-shrink-0 w-12 h-12 bg-retro-blue rounded-full flex items-center justify-center text-2xl">
            👩‍🔬
          </div>
          <div className="flex-1">
            <div className="font-bold text-retro-brown mb-1">
              アヤメ（統計分析担当）
            </div>
            <div className="bg-white p-4 rounded-lg shadow-sm text-sm text-retro-dark-gray leading-relaxed">
              「まずは基本から！各馬が1着になる確率を予測して、
              上位3頭を3連単として選ぶ方法だよ。
              LightGBMっていう機械学習モデルで、過去の成績・騎手・馬場状態を学習するの。」
            </div>
          </div>
        </div>

        {/* アルゴの発言 */}
        <div className="flex gap-3">
          <div className="flex-shrink-0 w-12 h-12 bg-retro-crimson rounded-full flex items-center justify-center text-2xl">
            🤖
          </div>
          <div className="flex-1">
            <div className="font-bold text-retro-brown mb-1">
              アルゴ（AI擬人化）
            </div>
            <div className="bg-white p-4 rounded-lg shadow-sm text-sm text-retro-dark-gray leading-relaxed">
              「僕が見てるのは、馬の過去勝率、騎手の成績、距離適性、馬場状態...
              約30個の特徴量だ。8,718レースのデータから学習して、
              『この馬は15%の確率で勝つ』って予測するんだ。」
            </div>
          </div>
        </div>

        {/* アヤメの発言 */}
        <div className="flex gap-3">
          <div className="flex-shrink-0 w-12 h-12 bg-retro-blue rounded-full flex items-center justify-center text-2xl">
            👩‍🔬
          </div>
          <div className="flex-1">
            <div className="font-bold text-retro-brown mb-1">アヤメ</div>
            <div className="bg-white p-4 rounded-lg shadow-sm text-sm text-retro-dark-gray leading-relaxed">
              「ただし注意点があるの。1着を当てるのと、3連単を当てるのは別問題。
              1着の予測精度が高くても、2着・3着の順番まで当てるのは難しい...
              でも、これが基本中の基本だから、まずはここから！」
            </div>
          </div>
        </div>

        {/* 学習ポイント */}
        <div className="bg-retro-blue/10 p-4 rounded-lg border-l-4 border-retro-blue">
          <div className="font-bold text-retro-brown mb-2">📚 学習ポイント</div>
          <ul className="text-sm text-retro-dark-gray space-y-1">
            <li>• LightGBMは決定木を組み合わせた機械学習モデル</li>
            <li>• クラス不均衡（1/8の馬しか勝たない）が課題</li>
            <li>• 1着予測と3連単予測は別のアプローチが必要</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
