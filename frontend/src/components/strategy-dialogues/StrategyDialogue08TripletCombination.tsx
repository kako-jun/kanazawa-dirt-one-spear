// 作戦8: 三連組合せ最適化 (triplet-combination)

export default function StrategyDialogue08TripletCombination() {
  return (
    <div className="newspaper-card p-6 mb-8 bg-gradient-to-br from-retro-wheat to-white">
      <h2 className="text-2xl font-serif font-bold text-retro-brown mb-4">
        🧮 作戦8「三連組合せ最適化」
      </h2>

      <div className="space-y-4">
        <div className="flex gap-3">
          <div className="flex-shrink-0 w-12 h-12 bg-retro-crimson rounded-full flex items-center justify-center text-2xl">
            🤖
          </div>
          <div className="flex-1">
            <div className="font-bold text-retro-brown mb-1">アルゴ</div>
            <div className="bg-white p-4 rounded-lg shadow-sm text-sm text-retro-dark-gray leading-relaxed">
              「各馬の1着・2着・3着確率を個別に予測してから、
              それらを掛け合わせて『最も確率の高い三連単』を計算する作戦だ。
              例: 馬Aが1着15% × 馬Bが2着20% × 馬Cが3着18% = 0.54%」
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
              「数学的には『確率の独立性』を仮定してるの。
              でも実際は、1着が決まると2着の確率も変わる（独立じゃない）。
              その矛盾をどう扱うかが課題だね。
              条件付き確率を使えば精度が上がるかも。」
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
              「全336通りの三連単を計算して、確率トップを選ぶ。
              計算コストは低いが、独立性の仮定が崩れると精度が落ちる。
              それでも、シンプルで理解しやすいのがメリットだ。」
            </div>
          </div>
        </div>

        <div className="bg-retro-gold/10 p-4 rounded-lg border-l-4 border-retro-gold">
          <div className="font-bold text-retro-brown mb-2">📚 学習ポイント</div>
          <ul className="text-sm text-retro-dark-gray space-y-1">
            <li>• 各馬の着順別確率を予測</li>
            <li>• 確率を掛け合わせて三連単確率を計算</li>
            <li>• 独立性の仮定が問題（条件付き確率で改善可能）</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
