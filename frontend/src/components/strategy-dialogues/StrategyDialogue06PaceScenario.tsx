// 作戦6: 展開予想型 (pace-scenario)

export default function StrategyDialogue06PaceScenario() {
  return (
    <div className="newspaper-card p-6 mb-8 bg-gradient-to-br from-retro-wheat to-white">
      <h2 className="text-2xl font-serif font-bold text-retro-brown mb-4">
        🏃 作戦6「展開予想型」
      </h2>

      <div className="space-y-4">
        <div className="flex gap-3">
          <div className="flex-shrink-0 w-12 h-12 bg-retro-crimson rounded-full flex items-center justify-center text-2xl">
            🤖
          </div>
          <div className="flex-1">
            <div className="font-bold text-retro-brown mb-1">アルゴ</div>
            <div className="bg-white p-4 rounded-lg shadow-sm text-sm text-retro-dark-gray leading-relaxed">
              「これは上級者向けの作戦だ。
              レース展開（ペース）を予測して、それに合った脚質の馬を選ぶ。
              例えば『スローペース→差し馬有利』『ハイペース→逃げ馬不利』って具合に。」
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
              「脚質っていうのは『逃げ・先行・差し・追込』の4タイプ。
              コーナー通過順位から推定できるの。
              逃げ馬が多いレースはハイペースになりやすいから、
              差し馬のチャンスが増える...って理論だね。」
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
              「課題は、脚質判定が難しいこと。
              データが不足してるから、まだ実験段階だ。
              でも、ハマれば強力な予想ができるはず。」
            </div>
          </div>
        </div>

        <div className="bg-retro-wheat/50 p-4 rounded-lg border-l-4 border-retro-brown">
          <div className="font-bold text-retro-brown mb-2">📚 学習ポイント</div>
          <ul className="text-sm text-retro-dark-gray space-y-1">
            <li>• ペース分析（スロー/ミドル/ハイ）</li>
            <li>• 脚質判定（逃げ/先行/差し/追込）</li>
            <li>• データ不足で実験段階（今後改善予定）</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
