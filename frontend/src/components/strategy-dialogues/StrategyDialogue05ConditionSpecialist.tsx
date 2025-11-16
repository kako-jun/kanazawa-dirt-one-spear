// 作戦5: 条件スペシャリスト (condition-specialist)

export default function StrategyDialogue05ConditionSpecialist() {
  return (
    <div className="newspaper-card p-6 mb-8 bg-gradient-to-br from-retro-wheat to-white">
      <h2 className="text-2xl font-serif font-bold text-retro-brown mb-4">
        ⚙️ 作戦5「条件スペシャリスト」
      </h2>

      <div className="space-y-4">
        <div className="flex gap-3">
          <div className="flex-shrink-0 w-12 h-12 bg-retro-blue rounded-full flex items-center justify-center text-2xl">
            👩‍🔬
          </div>
          <div className="flex-1">
            <div className="font-bold text-retro-brown mb-1">アヤメ</div>
            <div className="bg-white p-4 rounded-lg shadow-sm text-sm text-retro-dark-gray leading-relaxed">
              「『この条件なら強い！』って馬を探す作戦だよ。
              例えば、重馬場×1500mだと勝率30%の馬がいる。
              良馬場では10%なのに、条件が合うと化けるの。
              そういう『条件特化型』の馬を見つけるのが目標！」
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
              「統計テーブルから『馬場別勝率』『距離別勝率』『季節別勝率』を取得。
              今日のレース条件と照らし合わせて、
              『今日の条件ならこの馬だ』って判断する。
              条件が完璧に合った時の的中率は高いぞ。」
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
              「問題は、条件が合わないレースでは精度が下がること。
              『今日は該当する馬がいない』ってケースもある。
              でも、ハマった時の的中率は他の作戦より高いから、
              一長一短だね😊」
            </div>
          </div>
        </div>

        <div className="bg-retro-blue/10 p-4 rounded-lg border-l-4 border-retro-blue">
          <div className="font-bold text-retro-brown mb-2">📚 学習ポイント</div>
          <ul className="text-sm text-retro-dark-gray space-y-1">
            <li>• 馬場・距離・季節などの条件別統計を活用</li>
            <li>• 条件適性スコアを計算</li>
            <li>• 条件が合った時の高精度を狙う</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
