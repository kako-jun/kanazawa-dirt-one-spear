// 作戦1: 王道・勝率予測型 (basic-win-prob) - ブラッシュアップ版

export default function StrategyDialogue01BasicWinProb() {
  return (
    <div className="newspaper-card p-6 mb-8 bg-gradient-to-br from-retro-wheat to-white">
      <div className="flex items-center gap-3 mb-4">
        <span className="text-4xl">🎯</span>
        <div>
          <div className="text-sm text-retro-blue font-bold">STRATEGY #01</div>
          <h2 className="text-2xl font-serif font-bold text-retro-brown">
            王道・勝率予測型
          </h2>
          <div className="text-xs text-retro-dark-gray">Basic Win Probability</div>
        </div>
      </div>

      <div className="space-y-4">
        {/* アヤメの発言 */}
        <div className="flex gap-3">
          <div className="flex-shrink-0 w-12 h-12 bg-retro-blue rounded-full flex items-center justify-center text-2xl">
            👩‍🔬
          </div>
          <div className="flex-1">
            <div className="font-bold text-retro-brown mb-1 text-sm">
              アヤメ（統計分析担当）
            </div>
            <div className="bg-white p-4 rounded-lg shadow-sm text-sm text-retro-dark-gray leading-relaxed">
              「まずは基本中の基本から！各馬が1着になる確率を予測して、
              その上位3頭を『1着-2着-3着』として3連単予想を組み立てる方法だよ。
              <br /><br />
              例えば8頭のレースなら、1番の馬が勝つ確率18%、2番が12%、3番が25%...
              って全部予測するの。で、25%-18%-12%で『3-1-2』が本命！って決める感じ✨」
            </div>
          </div>
        </div>

        {/* アルゴの発言 */}
        <div className="flex gap-3">
          <div className="flex-shrink-0 w-12 h-12 bg-retro-crimson rounded-full flex items-center justify-center text-2xl">
            🤖
          </div>
          <div className="flex-1">
            <div className="font-bold text-retro-brown mb-1 text-sm">
              アルゴ（AI擬人化）
            </div>
            <div className="bg-white p-4 rounded-lg shadow-sm text-sm text-retro-dark-gray leading-relaxed">
              「僕が使ってるのは<strong className="text-retro-blue">LightGBM</strong>という機械学習モデル。
              決定木を何百本も組み合わせて予測する手法だ。
              <br /><br />
              見てる特徴量は約30個: 馬の過去成績（勝率、連対率）、騎手の腕前、
              馬場適性（良・稍重・重・不良での勝率）、距離適性、休養日数、馬齢、枠番...
              <br /><br />
              これらを総合して『この馬は15.3%の確率で勝つ』って算出してる。
              8,718レースのデータから学習した結果だ。」
            </div>
          </div>
        </div>

        {/* アヤメの発言 */}
        <div className="flex gap-3">
          <div className="flex-shrink-0 w-12 h-12 bg-retro-blue rounded-full flex items-center justify-center text-2xl">
            👩‍🔬
          </div>
          <div className="flex-1">
            <div className="font-bold text-retro-brown mb-1 text-sm">アヤメ</div>
            <div className="bg-white p-4 rounded-lg shadow-sm text-sm text-retro-dark-gray leading-relaxed">
              「ただし大きな問題点があるの！
              <br /><br />
              <span className="text-retro-crimson font-bold">問題1: クラス不均衡</span>
              <br />
              8頭立てなら、7頭は『負け』、1頭だけ『勝ち』。
              データが偏りすぎて学習が難しいのよね。
              <br /><br />
              <span className="text-retro-crimson font-bold">問題2: 順位は考慮されない</span>
              <br />
              『1着を当てる』と『2着・3着まで順番通り当てる』は全然別の問題。
              1着予測が上手くても、3連単的中率は低くなりがち...
              <br /><br />
              でも！これが予想の基礎だから、まずはここから始めるのが王道だよ😊」
            </div>
          </div>
        </div>

        {/* メリット・デメリット表 */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
          <div className="bg-retro-green/10 p-4 rounded-lg border-2 border-retro-green">
            <div className="font-bold text-retro-green mb-2 flex items-center gap-2">
              <span>✅</span>
              <span>メリット</span>
            </div>
            <ul className="text-xs text-retro-dark-gray space-y-1">
              <li>• 実装がシンプルで理解しやすい</li>
              <li>• LightGBMは高速で学習できる</li>
              <li>• なぜその予想をしたか説明可能（SHAP値）</li>
              <li>• 多くの機械学習の基礎となる手法</li>
            </ul>
          </div>

          <div className="bg-retro-crimson/10 p-4 rounded-lg border-2 border-retro-crimson">
            <div className="font-bold text-retro-crimson mb-2 flex items-center gap-2">
              <span>⚠️</span>
              <span>デメリット</span>
            </div>
            <ul className="text-xs text-retro-dark-gray space-y-1">
              <li>• クラス不均衡で学習が難しい</li>
              <li>• 1着予測≠3連単予測</li>
              <li>• 上位3頭が的中しても順番外れる</li>
              <li>• 作戦2の方が理論的に優れている</li>
            </ul>
          </div>
        </div>

        {/* 学習ポイント */}
        <div className="bg-retro-blue/10 p-4 rounded-lg border-l-4 border-retro-blue">
          <div className="font-bold text-retro-brown mb-2">📚 学習ポイント</div>
          <ul className="text-sm text-retro-dark-gray space-y-1">
            <li>
              • <strong>LightGBM</strong> = 勾配ブースティング決定木。高速で精度が高い
            </li>
            <li>
              • <strong>クラス不均衡</strong> = 正例（勝ち）が少ないデータの学習課題
            </li>
            <li>
              • <strong>二値分類</strong> = 「勝つ/負ける」の2択を予測する手法
            </li>
            <li>• 1着予測と順位予測は別問題。作戦2で改善される</li>
          </ul>
        </div>

        {/* 実装状況 */}
        <div className="bg-retro-gold/10 p-3 rounded-lg border-l-4 border-retro-gold text-sm">
          <div className="font-bold text-retro-brown mb-1">📊 実装状況</div>
          <div className="text-retro-dark-gray">
            <span className="inline-block px-2 py-1 bg-retro-green text-white text-xs rounded mr-2">
              実装済
            </span>
            <span className="text-xs">
              時系列交差検証で的中率・回収率を測定中。作戦2〜10と性能比較予定。
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}
