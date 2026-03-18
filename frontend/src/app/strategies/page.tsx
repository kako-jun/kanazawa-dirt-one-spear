'use client'

import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'
import StrategyDialogue01BasicWinProb from '@/components/strategy-dialogues/StrategyDialogue01BasicWinProb'
import StrategyDialogue02LearningToRank from '@/components/strategy-dialogues/StrategyDialogue02LearningToRank'
import StrategyDialogue03OddsValueHunter from '@/components/strategy-dialogues/StrategyDialogue03OddsValueHunter'
import StrategyDialogue04ComboAffinity from '@/components/strategy-dialogues/StrategyDialogue04ComboAffinity'
import StrategyDialogue05ConditionSpecialist from '@/components/strategy-dialogues/StrategyDialogue05ConditionSpecialist'
import StrategyDialogue06PaceScenario from '@/components/strategy-dialogues/StrategyDialogue06PaceScenario'
import StrategyDialogue07TrifectaPattern from '@/components/strategy-dialogues/StrategyDialogue07TrifectaPattern'
import StrategyDialogue08TripletCombination from '@/components/strategy-dialogues/StrategyDialogue08TripletCombination'
import StrategyDialogue09NoOddsPure from '@/components/strategy-dialogues/StrategyDialogue09NoOddsPure'
import StrategyDialogue10WithOddsHybrid from '@/components/strategy-dialogues/StrategyDialogue10WithOddsHybrid'
import OccultVerificationSection from '@/components/verification/OccultVerificationSection'

export default function StrategiesPage() {
  return (
    <div className="min-h-screen flex flex-col bg-retro-sepia">
      <Header />

      <main className="flex-1 py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl md:text-4xl font-serif font-bold text-retro-brown mb-4">
            予想の10の作戦
          </h1>
          <p className="text-retro-dark-gray mb-8 leading-relaxed">
            金沢ダート一本槍は、複数の予想アプローチを実験しています。
            <br />
            それぞれの作戦を、アヤメとアルゴの会話で分かりやすく解説します。
          </p>

          {/* キャラクター紹介 */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div className="newspaper-card p-6 text-center">
              <div className="w-20 h-20 bg-retro-blue rounded-full flex items-center justify-center text-4xl mx-auto mb-3">
                👩‍🔬
              </div>
              <h3 className="text-lg font-bold text-retro-brown mb-2">
                アヤメ（統計分析担当）
              </h3>
              <p className="text-sm text-retro-dark-gray">
                真面目でデータ大好き。
                <br />
                難しい統計学を分かりやすく説明してくれます。
              </p>
            </div>

            <div className="newspaper-card p-6 text-center">
              <div className="w-20 h-20 bg-retro-crimson rounded-full flex items-center justify-center text-4xl mx-auto mb-3">
                🤖
              </div>
              <h3 className="text-lg font-bold text-retro-brown mb-2">
                アルゴ（AI擬人化）
              </h3>
              <p className="text-sm text-retro-dark-gray">
                冷静沈着で論理的。
                <br />
                AIの判断プロセスを人間の言葉で伝えてくれます。
              </p>
            </div>
          </div>

          {/* 作戦一覧 */}
          <div className="space-y-8">
            <StrategyDialogue01BasicWinProb />
            <StrategyDialogue02LearningToRank />
            <StrategyDialogue03OddsValueHunter />
            <StrategyDialogue04ComboAffinity />
            <StrategyDialogue05ConditionSpecialist />
            <StrategyDialogue06PaceScenario />
            <StrategyDialogue07TrifectaPattern />
            <StrategyDialogue08TripletCombination />
            <StrategyDialogue09NoOddsPure />
            <StrategyDialogue10WithOddsHybrid />
          </div>

          {/* 作戦比較表 */}
          <div className="newspaper-card p-6 mt-12 bg-retro-blue/10">
            <h2 className="text-2xl font-serif font-bold text-retro-brown mb-4">
              📊 作戦の比較
            </h2>
            <p className="text-sm text-retro-dark-gray mb-4">
              各作戦は時系列交差検証で性能を測定し、比較しています。
            </p>

            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-retro-brown text-white">
                    <th className="p-3 text-left">作戦</th>
                    <th className="p-3 text-center">状態</th>
                    <th className="p-3 text-center">優先度</th>
                    <th className="p-3 text-center">特徴</th>
                  </tr>
                </thead>
                <tbody className="bg-retro-sepia">
                  <tr className="border-b">
                    <td className="p-3">1. 王道・勝率予測型</td>
                    <td className="p-3 text-center">
                      <span className="px-2 py-1 bg-retro-green text-white text-xs rounded">
                        実装済
                      </span>
                    </td>
                    <td className="p-3 text-center">基本</td>
                    <td className="p-3 text-xs">シンプル、理解しやすい</td>
                  </tr>
                  <tr className="border-b">
                    <td className="p-3">2. 順位予測型</td>
                    <td className="p-3 text-center">
                      <span className="px-2 py-1 bg-retro-gold text-white text-xs rounded">
                        開発中
                      </span>
                    </td>
                    <td className="p-3 text-center">高</td>
                    <td className="p-3 text-xs">理論的に最適</td>
                  </tr>
                  <tr className="border-b">
                    <td className="p-3">3. 穴馬ハンター</td>
                    <td className="p-3 text-center">
                      <span className="px-2 py-1 bg-retro-gold text-white text-xs rounded">
                        開発中
                      </span>
                    </td>
                    <td className="p-3 text-center">高</td>
                    <td className="p-3 text-xs">高配当狙い</td>
                  </tr>
                  <tr className="border-b">
                    <td className="p-3">4. 相性重視型</td>
                    <td className="p-3 text-center">
                      <span className="px-2 py-1 bg-retro-blue text-white text-xs rounded">
                        計画中
                      </span>
                    </td>
                    <td className="p-3 text-center">中</td>
                    <td className="p-3 text-xs">安定性重視</td>
                  </tr>
                  <tr className="border-b">
                    <td className="p-3">5. 条件スペシャリスト</td>
                    <td className="p-3 text-center">
                      <span className="px-2 py-1 bg-retro-blue text-white text-xs rounded">
                        計画中
                      </span>
                    </td>
                    <td className="p-3 text-center">中</td>
                    <td className="p-3 text-xs">条件特化</td>
                  </tr>
                  <tr className="border-b">
                    <td className="p-3">6. 展開予想型</td>
                    <td className="p-3 text-center">
                      <span className="px-2 py-1 bg-gray-400 text-white text-xs rounded">
                        検討中
                      </span>
                    </td>
                    <td className="p-3 text-center">低</td>
                    <td className="p-3 text-xs">上級者向け</td>
                  </tr>
                  <tr className="border-b">
                    <td className="p-3">7. 三連単パターン学習</td>
                    <td className="p-3 text-center">
                      <span className="px-2 py-1 bg-retro-blue text-white text-xs rounded">
                        計画中
                      </span>
                    </td>
                    <td className="p-3 text-center">中</td>
                    <td className="p-3 text-xs">実験的</td>
                  </tr>
                  <tr className="border-b">
                    <td className="p-3">8. 三連組合せ最適化</td>
                    <td className="p-3 text-center">
                      <span className="px-2 py-1 bg-retro-blue text-white text-xs rounded">
                        計画中
                      </span>
                    </td>
                    <td className="p-3 text-center">中</td>
                    <td className="p-3 text-xs">確率計算</td>
                  </tr>
                  <tr className="border-b">
                    <td className="p-3">9. オッズ無視型</td>
                    <td className="p-3 text-center">
                      <span className="px-2 py-1 bg-retro-gold text-white text-xs rounded">
                        実験中
                      </span>
                    </td>
                    <td className="p-3 text-center">高</td>
                    <td className="p-3 text-xs">独自性重視</td>
                  </tr>
                  <tr>
                    <td className="p-3">10. オッズ考慮型</td>
                    <td className="p-3 text-center">
                      <span className="px-2 py-1 bg-retro-gold text-white text-xs rounded">
                        実験中
                      </span>
                    </td>
                    <td className="p-3 text-center">高</td>
                    <td className="p-3 text-xs">集合知活用</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <p className="text-xs text-retro-brown mt-4">
              ※ 各作戦は時系列交差検証で性能を測定し、最適な手法を選定中です
            </p>
          </div>
        </div>
      </main>

      {/* オカルト検証コーナー */}
      <OccultVerificationSection />

      <Footer />
    </div>
  )
}
