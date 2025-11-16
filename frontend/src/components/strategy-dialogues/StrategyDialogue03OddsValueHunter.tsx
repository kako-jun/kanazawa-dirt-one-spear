// 作戦3: 穴馬ハンター (odds-value-hunter)

export default function StrategyDialogue03OddsValueHunter() {
  return (
    <div className="newspaper-card p-6 mb-8 bg-gradient-to-br from-retro-wheat to-white">
      <h2 className="text-2xl font-serif font-bold text-retro-brown mb-4">
        💎 作戦3「穴馬ハンター」
      </h2>

      <div className="space-y-4">
        <div className="flex gap-3">
          <div className="flex-shrink-0 w-12 h-12 bg-retro-blue rounded-full flex items-center justify-center text-2xl">
            👩‍🔬
          </div>
          <div className="flex-1">
            <div className="font-bold text-retro-brown mb-1">アヤメ</div>
            <div className="bg-white p-4 rounded-lg shadow-sm text-sm text-retro-dark-gray leading-relaxed">
              「『オッズと実力の乖離を突く』作戦だよ！
              人間は有名騎手や前走1着の馬を過大評価しがち。
              逆に、地味だけど実力がある馬は過小評価される。
              その『見落とされた馬』を見つけるの。」
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
              「僕がデータから見た『本当の勝率15%』の馬が、
              オッズでは人気薄の50倍になってることがある。
              それが狙い目だ。期待値で言えば、100円が750円のリターン。
              オッズ1.5倍の本命より価値がある。」
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
              「これは『バリュー投資』って考え方ね。株式投資でも同じ。
              みんなが見落としてる優良銘柄を探す。
              当たれば高配当！でも外れリスクも高いから、諸刃の剣だよ😅」
            </div>
          </div>
        </div>

        <div className="bg-retro-crimson/10 p-4 rounded-lg border-l-4 border-retro-crimson">
          <div className="font-bold text-retro-brown mb-2">📚 学習ポイント</div>
          <ul className="text-sm text-retro-dark-gray space-y-1">
            <li>• オッズバイアス（人間の集団的思い込み）を利用</li>
            <li>• 期待値が高い馬を選択</li>
            <li>• 高配当狙いだが的中率は下がる可能性</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
