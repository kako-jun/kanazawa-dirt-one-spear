// 作戦2: 順位予測型 (learning-to-rank)

export default function StrategyDialogue02LearningToRank() {
  return (
    <div className="newspaper-card p-6 mb-8 bg-gradient-to-br from-retro-wheat to-white">
      <h2 className="text-2xl font-serif font-bold text-retro-brown mb-4">
        🏆 作戦2「順位予測型」
      </h2>

      <div className="space-y-4">
        <div className="flex gap-3">
          <div className="flex-shrink-0 w-12 h-12 bg-retro-crimson rounded-full flex items-center justify-center text-2xl">
            🤖
          </div>
          <div className="flex-1">
            <div className="font-bold text-retro-brown mb-1">アルゴ</div>
            <div className="bg-white p-4 rounded-lg shadow-sm text-sm text-retro-dark-gray leading-relaxed">
              「作戦1の問題点に気づいた。『勝つか負けるか』じゃなくて、
              『何着になるか』を直接予測すべきだ。
              ランキング学習という手法で、レース内の順位を予測する。」
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
              「LambdaMARTっていう、Googleの検索ランキングにも使われてる技術なの。
              馬を『検索結果』に見立てて、順位をつける。
              『この馬は2着相当、あの馬は5着相当』って直接判断できるのが強み！」
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
              「理論的には、3連単予想に最も適したアプローチだ。
              ただし、データの準備が複雑で、計算コストも高い。
              でも、精度が上がるなら試す価値は十分にある。」
            </div>
          </div>
        </div>

        <div className="bg-retro-gold/10 p-4 rounded-lg border-l-4 border-retro-gold">
          <div className="font-bold text-retro-brown mb-2">📚 学習ポイント</div>
          <ul className="text-sm text-retro-dark-gray space-y-1">
            <li>• ランキング学習は順位を直接予測する手法</li>
            <li>• LambdaMART/LightGBM Rankerを使用</li>
            <li>• 3連単予想に理論的に最適</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
