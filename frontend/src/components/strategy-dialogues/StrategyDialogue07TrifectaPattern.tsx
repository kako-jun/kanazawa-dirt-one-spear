// 作戦7: 三連単パターン学習 (trifecta-pattern-learning)

export default function StrategyDialogue07TrifectaPattern() {
  return (
    <div className="newspaper-card p-6 mb-8 bg-gradient-to-br from-retro-wheat to-white">
      <h2 className="text-2xl font-serif font-bold text-retro-brown mb-4">
        🎨 作戦7「三連単パターン学習」
      </h2>

      <div className="space-y-4">
        <div className="flex gap-3">
          <div className="flex-shrink-0 w-12 h-12 bg-retro-blue rounded-full flex items-center justify-center text-2xl">
            👩‍🔬
          </div>
          <div className="flex-1">
            <div className="font-bold text-retro-brown mb-1">アヤメ</div>
            <div className="bg-white p-4 rounded-lg shadow-sm text-sm text-retro-dark-gray leading-relaxed">
              「ちょっと視点を変えた作戦だよ！
              『1-3-5』『2-4-7』みたいな三連単の組み合わせパターンを直接学習するの。
              『内-中-外』『人気-中穴-大穴』みたいなパターンが存在するかも...って発想。」
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
              「過去8,718レースの三連単パターンを分析。
              例えば『1着は内枠、2着は人気馬、3着は穴馬』って組み合わせが多い...
              みたいな傾向を見つけ出す。
              ディープラーニングで複雑なパターンも学習できる。」
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
              「リスクは『組み合わせ爆発』。
              8頭立てでも336通りの三連単がある。
              パターンが多すぎて学習が難しいかも...
              でも、成功すれば画期的な予想ができる！実験的作戦だね😊」
            </div>
          </div>
        </div>

        <div className="bg-retro-crimson/10 p-4 rounded-lg border-l-4 border-retro-crimson">
          <div className="font-bold text-retro-brown mb-2">📚 学習ポイント</div>
          <ul className="text-sm text-retro-dark-gray space-y-1">
            <li>• 三連単の組み合わせパターンを直接学習</li>
            <li>• 枠番・人気・脚質の組み合わせ傾向を分析</li>
            <li>• 組み合わせ爆発が課題（実験的手法）</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
