// 作戦4: 相性重視型 (combo-affinity)

export default function StrategyDialogue04ComboAffinity() {
  return (
    <div className="newspaper-card p-6 mb-8 bg-gradient-to-br from-retro-wheat to-white">
      <h2 className="text-2xl font-serif font-bold text-retro-brown mb-4">
        🤝 作戦4「相性重視型」
      </h2>

      <div className="space-y-4">
        <div className="flex gap-3">
          <div className="flex-shrink-0 w-12 h-12 bg-retro-crimson rounded-full flex items-center justify-center text-2xl">
            🤖
          </div>
          <div className="flex-1">
            <div className="font-bold text-retro-brown mb-1">アルゴ</div>
            <div className="bg-white p-4 rounded-lg shadow-sm text-sm text-retro-dark-gray leading-relaxed">
              「馬×騎手の相性を重視する作戦だ。
              騎手Aは全体勝率15%だが、馬Xに乗ると25%に上がる...
              そういう『相性の良い組み合わせ』を統計から見つける。」
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
              「競馬には『手綱が合う』『呼吸が合う』って表現があるの。
              統計的にも確かに相性はあるみたい。
              ただし、最低10回以上のコンビ実績がないと信頼できない。
              偶然かもしれないからね。」
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
              「調教師×馬、馬場×馬、距離×馬...
              色々な組み合わせで相性スコアを計算する。
              全部を統合して『この組み合わせは信頼できる』って判断するんだ。」
            </div>
          </div>
        </div>

        <div className="bg-retro-green/10 p-4 rounded-lg border-l-4 border-retro-green">
          <div className="font-bold text-retro-brown mb-2">📚 学習ポイント</div>
          <ul className="text-sm text-retro-dark-gray space-y-1">
            <li>• 馬×騎手、馬×調教師、馬×馬場などの相性分析</li>
            <li>• 最低実績数でフィルタリング（偶然排除）</li>
            <li>• 相性スコアを特徴量として活用</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
