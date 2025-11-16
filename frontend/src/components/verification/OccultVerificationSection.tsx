// オカルト検証コーナー - 動的に増えていくコンテンツ

interface OccultVerification {
  id: string
  title: string
  hypothesis: string
  method: string
  result: 'confirmed' | 'rejected' | 'inconclusive'
  pValue?: number
  description: string
  date: string
}

// 検証結果データ（将来的にはAPIから取得）
const verifications: OccultVerification[] = [
  {
    id: '001',
    title: '満月の日は荒れる？',
    hypothesis: '満月・新月の日は波乱（人気薄の勝利）が多い',
    method: 'カイ二乗検定で月齢と波乱度の関連性を検証',
    result: 'rejected',
    pValue: 0.87,
    description:
      '8,718レースを月齢別に分類して分析。満月（±2日）のレースと通常のレースで、1-3番人気以外の勝率を比較。結果、統計的有意差なし（p=0.87）。満月は競馬に影響しないことが判明。',
    date: '2025-11-10',
  },
  {
    id: '002',
    title: '馬名に「王」が入ると強い？',
    hypothesis: '縁起の良い漢字が入った馬名は勝率が高い',
    method: '馬名に含まれる漢字別の勝率を集計・比較',
    result: 'rejected',
    pValue: 0.54,
    description:
      '「王」「龍」「鳳」「金」などの縁起の良い漢字を含む馬名を抽出。それぞれの勝率を全体平均と比較。どの漢字も統計的有意差なし（p=0.54）。馬名のジンクスは迷信と結論。',
    date: '2025-11-12',
  },
  {
    id: '003',
    title: '雨の日は内枠有利？',
    hypothesis: '重馬場・不良馬場では内枠（1-3枠）が有利',
    method: '馬場状態×枠番の2元配置分散分析',
    result: 'confirmed',
    pValue: 0.023,
    description:
      '重馬場・不良馬場のレースで枠番別勝率を分析。内枠（1-3枠）の勝率が統計的に有意に高い（p=0.023）。雨で外を回る不利が顕著に。この知見は予想に活用する価値あり！',
    date: '2025-11-14',
  },
]

export default function OccultVerificationSection() {
  return (
    <section className="py-12 md:py-16 bg-retro-sepia">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl md:text-4xl font-serif font-bold text-retro-brown text-center mb-4">
          意外なことを検証しました
        </h2>
        <p className="text-center text-retro-dark-gray mb-8 leading-relaxed">
          「オカルト」と言われる競馬の噂を統計で検証。
          <br className="hidden sm:inline" />
          効果がなければ迷信、効果があれば予想に活用します。
        </p>

        <div className="space-y-6">
          {verifications.map((verification) => {
            const resultConfig = {
              confirmed: {
                bgColor: 'bg-retro-green/10',
                borderColor: 'border-retro-green',
                textColor: 'text-retro-green',
                icon: '✅',
                label: '効果あり！',
              },
              rejected: {
                bgColor: 'bg-retro-dark-gray/10',
                borderColor: 'border-retro-dark-gray',
                textColor: 'text-retro-dark-gray',
                icon: '❌',
                label: '効果なし',
              },
              inconclusive: {
                bgColor: 'bg-retro-gold/10',
                borderColor: 'border-retro-gold',
                textColor: 'text-retro-gold',
                icon: '🤔',
                label: '判定保留',
              },
            }

            const config = resultConfig[verification.result]

            return (
              <div
                key={verification.id}
                className={`newspaper-card p-6 ${config.bgColor} border-2 ${config.borderColor}`}
              >
                <div className="flex flex-col md:flex-row md:items-start justify-between gap-4 mb-4">
                  <div className="flex-1">
                    <h3 className="text-xl font-serif font-bold text-retro-brown mb-2">
                      {verification.title}
                    </h3>
                    <div className="text-sm text-retro-dark-gray mb-2">
                      <span className="font-bold">仮説: </span>
                      {verification.hypothesis}
                    </div>
                  </div>

                  <div
                    className={`flex items-center gap-2 px-4 py-2 ${config.bgColor} border-2 ${config.borderColor} rounded-lg`}
                  >
                    <span className="text-2xl">{config.icon}</span>
                    <span className={`font-bold ${config.textColor}`}>
                      {config.label}
                    </span>
                  </div>
                </div>

                <div className="bg-white p-4 rounded-lg mb-4">
                  <div className="text-sm mb-3">
                    <span className="font-bold text-retro-brown">検証方法: </span>
                    <span className="text-retro-dark-gray">{verification.method}</span>
                  </div>

                  {verification.pValue !== undefined && (
                    <div className="text-sm mb-3">
                      <span className="font-bold text-retro-brown">p値: </span>
                      <span className="font-mono text-retro-dark-gray">
                        {verification.pValue.toFixed(3)}
                      </span>
                      <span className="text-xs text-gray-600 ml-2">
                        （0.05以下で統計的に有意）
                      </span>
                    </div>
                  )}

                  <div className="text-sm">
                    <span className="font-bold text-retro-brown">結果: </span>
                    <span className="text-retro-dark-gray leading-relaxed">
                      {verification.description}
                    </span>
                  </div>
                </div>

                <div className="flex items-center justify-between text-xs text-retro-brown">
                  <span>検証ID: #{verification.id}</span>
                  <span>検証日: {verification.date}</span>
                </div>
              </div>
            )
          })}
        </div>

        {/* アヤメ×アルゴの解説 */}
        <div className="newspaper-card p-6 mt-8 bg-gradient-to-br from-retro-wheat to-white">
          <h3 className="text-xl font-serif font-bold text-retro-brown mb-4">
            🔬 検証の裏側
          </h3>

          <div className="space-y-4">
            <div className="flex gap-3">
              <div className="flex-shrink-0 w-12 h-12 bg-retro-blue rounded-full flex items-center justify-center text-2xl">
                👩‍🔬
              </div>
              <div className="flex-1">
                <div className="font-bold text-retro-brown mb-1">アヤメ</div>
                <div className="bg-white p-4 rounded-lg shadow-sm text-sm text-retro-dark-gray leading-relaxed">
                  「オカルトって馬鹿にできないの。
                  もしかしたら本当に効果があるかもしれないから、統計でちゃんと検証してる。
                  『満月で荒れる』は迷信だったけど、『雨で内枠有利』は本当だった！
                  この差が大事なんだよね😊」
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
                  「僕は偏見を持たない。どんな仮説も公平に検証する。
                  効果があれば予想に取り入れ、なければ捨てる。
                  それだけだ。『雨で内枠有利』は今後の予想に活用していくぞ。」
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* 今後の検証予定 */}
        <div className="mt-8 text-center newspaper-card p-6">
          <h3 className="text-lg font-bold text-retro-brown mb-3">
            📋 今後の検証予定
          </h3>
          <ul className="text-sm text-retro-dark-gray space-y-2 max-w-2xl mx-auto text-left">
            <li className="flex items-start gap-2">
              <span className="text-retro-blue">•</span>
              <span>血統に「キング」が入ると強い？（父馬名の分析）</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-retro-blue">•</span>
              <span>金曜日のレースは荒れる？（曜日別波乱度）</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-retro-blue">•</span>
              <span>騎手の誕生月と成績の関連性（星座占い検証）</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-retro-blue">•</span>
              <span>馬齢と距離適性の関係（若馬は短距離有利？）</span>
            </li>
          </ul>
          <p className="text-xs text-retro-brown mt-4">
            ※ 新しい検証結果は随時追加されます
          </p>
        </div>
      </div>
    </section>
  )
}
