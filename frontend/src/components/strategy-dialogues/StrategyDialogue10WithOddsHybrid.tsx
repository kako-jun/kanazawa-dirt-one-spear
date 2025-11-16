// 作戦10: オッズ考慮型 (with-odds-hybrid)

export default function StrategyDialogue10WithOddsHybrid() {
  return (
    <div className="newspaper-card p-6 mb-8 bg-gradient-to-br from-retro-wheat to-white">
      <h2 className="text-2xl font-serif font-bold text-retro-brown mb-4">
        🎭 作戦10「オッズ考慮型」
      </h2>

      <div className="space-y-4">
        <div className="flex gap-3">
          <div className="flex-shrink-0 w-12 h-12 bg-retro-crimson rounded-full flex items-center justify-center text-2xl">
            🤖
          </div>
          <div className="flex-1">
            <div className="font-bold text-retro-brown mb-1">アルゴ</div>
            <div className="bg-white p-4 rounded-lg shadow-sm text-sm text-retro-dark-gray leading-relaxed">
              「作戦9の対極。オッズ（人間の集合知）も特徴量として使う。
              客観的データ + 人間の予想 = ハイブリッド予想。
              人間の知恵には意味があるという立場だ。」
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
              「オッズには『現地の情報』『調教の評判』『馬体の状態』とか、
              データに現れない情報が反映されてる可能性があるの。
              それを活用すれば、精度が上がるかも...
              でも、人間のバイアスに引きずられるリスクもあるよね。」
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
              「統計的には、オッズ考慮型の方が的中率は高くなる傾向。
              でも、配当が下がるから回収率は微妙。
              作戦9と作戦10、どっちが最終的に儲かるか...
              それが最大の実験テーマだ。」
            </div>
          </div>
        </div>

        <div className="bg-retro-gold/10 p-4 rounded-lg border-l-4 border-retro-gold">
          <div className="font-bold text-retro-brown mb-2">📚 学習ポイント</div>
          <ul className="text-sm text-retro-dark-gray space-y-1">
            <li>• オッズ・人気順を特徴量に含める</li>
            <li>• 人間の集合知を活用</li>
            <li>• 的中率↑、配当↓の傾向（回収率は要検証）</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
