// 作戦9: オッズ無視型 (no-odds-pure)

export default function StrategyDialogue09NoOddsPure() {
  return (
    <div className="newspaper-card p-6 mb-8 bg-gradient-to-br from-retro-wheat to-white">
      <h2 className="text-2xl font-serif font-bold text-retro-brown mb-4">
        🔍 作戦9「オッズ無視型」
      </h2>

      <div className="space-y-4">
        <div className="flex gap-3">
          <div className="flex-shrink-0 w-12 h-12 bg-retro-blue rounded-full flex items-center justify-center text-2xl">
            👩‍🔬
          </div>
          <div className="flex-1">
            <div className="font-bold text-retro-brown mb-1">アヤメ</div>
            <div className="bg-white p-4 rounded-lg shadow-sm text-sm text-retro-dark-gray leading-relaxed">
              「これは哲学的な実験だよ！
              オッズ（人間の予想）を一切見ずに、客観的データだけで予想する。
              『AIは大穴を知らない』。全ての馬を平等に、データだけで評価するの。」
            </div>
          </div>
        </div>

        <div className="flex gap-3">
          <div className="flex-shrink-0 w-12 h-12 bg-retro-crimson rounded-full flex items-center justify-center text-2xl">
            🤖
          </div>
          <div className="flex-1">
            <div className="font-bold text-retro-brown mb-1">アルゴ</div>
            <div className="bg-white p-4 rounded-lg shadow-sm text-sm text-retro-dark-gray leading-relaxed">
              「僕が見てるのは、過去成績・血統・騎手・馬場・距離...
              オッズは完全に無視。
              人間が50倍の大穴と思ってる馬でも、僕が『勝率20%』と判断すれば本命にする。
              人間のバイアスに影響されない純粋な予想だ。」
            </div>
          </div>
        </div>

        <div className="flex gap-3">
          <div className="flex-shrink-0 w-12 h-12 bg-retro-blue rounded-full flex items-center justify-center text-2xl">
            👩‍🔬
          </div>
          <div className="flex-1">
            <div className="font-bold text-retro-brown mb-1">アヤメ</div>
            <div className="bg-white p-4 rounded-lg shadow-sm text-sm text-retro-dark-gray leading-relaxed">
              「メリットは『見落とされた馬』を発見できること。
              デメリットは『人間の集合知』を捨ててること。
              作戦10のオッズ考慮型と比較して、どちらが優れてるか実験中だよ😊」
            </div>
          </div>
        </div>

        <div className="bg-retro-blue/10 p-4 rounded-lg border-l-4 border-retro-blue">
          <div className="font-bold text-retro-brown mb-2">📚 学習ポイント</div>
          <ul className="text-sm text-retro-dark-gray space-y-1">
            <li>• オッズ（人間の予想）を特徴量から除外</li>
            <li>• 人間のバイアスに影響されない</li>
            <li>• 過小評価馬を発見できる可能性</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
