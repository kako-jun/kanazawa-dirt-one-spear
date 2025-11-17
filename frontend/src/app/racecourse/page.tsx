'use client'

import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'

export default function RacecoursePage() {
  const facilities = [
    {
      title: 'レトロな食堂',
      emoji: '🍛',
      description:
        '昭和の香り漂う競馬場の食堂。メニューはカツカレー¥500、ラーメン¥400など、庶民的な価格。ボロボロだけど、それがいい。レース観戦の合間に、懐かしい味を楽しめます。',
      features: [
        'カツカレー ¥500',
        'ラーメン ¥400',
        'うどん・そば各種',
        '昭和レトロな雰囲気',
        '安くて美味しい',
      ],
    },
    {
      title: 'スタンド',
      emoji: '🏟️',
      description:
        '年季の入ったコンクリート造りのスタンド。レースを間近で見られる迫力は格別。芝生エリアもあり、ピクニック気分で楽しめます。',
      features: [
        '屋内観覧席',
        '屋外芝生エリア',
        'パドック一体型',
        '間近で見る迫力',
        '家族連れでも安心',
      ],
    },
    {
      title: '中央公園へ続くトンネル',
      emoji: '🚶',
      description:
        'スタンドから中央公園へ続く薄暗いトンネル。レース前の静寂、期待と緊張。馬券を握りしめて歩く道。このトンネルを抜けると、別世界が広がります。',
      features: [
        '薄暗い独特の雰囲気',
        'レース前の緊張感',
        '競馬場の裏側',
        'フォトスポット',
      ],
    },
    {
      title: '中央公園の憩い',
      emoji: '🌳',
      description:
        'トンネルを抜けると広がる緑豊かな公園。家族連れで賑わい、子供が遊び、大人は馬券を研究。競馬場のもう一つの顔。ピクニックシートを広げてのんびり過ごせます。',
      features: [
        '緑豊かな広場',
        '家族連れで楽しめる',
        'ピクニック気分',
        '子供の遊び場',
        '無料休憩スペース',
      ],
    },
    {
      title: 'パドック',
      emoji: '🐴',
      description:
        'レース前に馬の状態を確認できるパドック。間近で見る馬の筋肉美、歩様、気合い。ここで馬を見極めてから馬券を買うのが通の楽しみ方。',
      features: [
        '馬を間近で観察',
        '歩様チェック',
        '気合いを確認',
        '騎手の表情も見える',
      ],
    },
    {
      title: '投票所',
      emoji: '🎫',
      description:
        '券売機が並ぶ投票所。紙の馬券を手に取る瞬間のワクワク感。最近はオンライン購入も便利ですが、現地で買う馬券は特別です。',
      features: [
        '自動券売機完備',
        'マークカード方式',
        '現金のみ対応',
        '窓口スタッフ常駐',
      ],
    },
  ]

  const access = [
    {
      method: '🚗 自動車',
      details: [
        '北陸自動車道「金沢西IC」から約15分',
        '金沢駅から約20分',
        '無料駐車場完備（約800台）',
      ],
    },
    {
      method: '🚌 バス',
      details: [
        '金沢駅から北鉄バス「競馬場前」下車',
        '所要時間：約30分',
        '開催日は臨時便あり',
      ],
    },
    {
      method: '🚲 自転車',
      details: ['駐輪場完備', '金沢市内から気軽にアクセス'],
    },
  ]

  const schedule = [
    { day: '火曜日', note: '通常開催' },
    { day: '水曜日', note: '通常開催' },
    { day: '木曜日', note: '通常開催' },
    { day: '金曜日', note: '通常開催' },
    { day: '土曜日', note: 'ファミリーデー' },
    { day: '日曜日', note: '特別レース多数' },
  ]

  return (
    <div className="min-h-screen flex flex-col bg-retro-sepia">
      <Header />

      <main className="flex-1 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl md:text-4xl font-serif font-bold text-retro-brown mb-8">
            金沢競馬場のいいところ
          </h1>

          {/* キャッチコピー */}
          <div className="newspaper-card p-8 mb-8 text-center bg-gradient-to-br from-retro-wheat to-white">
            <h2 className="text-2xl md:text-3xl font-serif font-bold text-retro-brown mb-4">
              昭和レトロな雰囲気が残る、温かみのある競馬場
            </h2>
            <p className="text-retro-dark-gray max-w-2xl mx-auto leading-relaxed">
              金沢競馬場は、北陸唯一の地方競馬場。
              最新設備ではないけれど、だからこそ人間味があり、
              馬や騎手との距離が近い。ボロボロの食堂も、薄暗いトンネルも、
              全てが金沢競馬の魅力です。
            </p>
          </div>

          {/* 施設紹介 */}
          <div className="mb-12">
            <h2 className="text-2xl font-serif font-bold text-retro-brown mb-6">
              施設紹介
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {facilities.map((facility, index) => (
                <div
                  key={index}
                  className="newspaper-card p-6 hover:shadow-xl transition-shadow"
                >
                  {/* 画像プレースホルダー */}
                  <div className="bg-retro-wheat border-2 border-retro-brown h-48 rounded-lg mb-4 flex items-center justify-center">
                    <div className="text-retro-brown text-center">
                      <div className="text-5xl mb-2">{facility.emoji}</div>
                      <div className="text-sm opacity-75">写真準備中</div>
                    </div>
                  </div>

                  {/* タイトル */}
                  <h3 className="text-xl font-serif font-bold text-retro-brown mb-3">
                    {facility.title}
                  </h3>

                  {/* 説明 */}
                  <p className="text-sm text-retro-dark-gray mb-4 leading-relaxed">
                    {facility.description}
                  </p>

                  {/* 特徴 */}
                  <div className="space-y-1">
                    {facility.features.map((feature, fIndex) => (
                      <div key={fIndex} className="flex items-start gap-2 text-sm">
                        <span className="text-retro-green font-bold">✓</span>
                        <span className="text-retro-brown">{feature}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* アクセス */}
          <div className="newspaper-card p-8 mb-8">
            <h2 className="text-2xl font-serif font-bold text-retro-brown mb-6">
              アクセス
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {access.map((item, index) => (
                <div key={index} className="bg-white p-5 rounded-lg">
                  <h3 className="text-lg font-bold text-retro-brown mb-3">
                    {item.method}
                  </h3>
                  <ul className="space-y-2">
                    {item.details.map((detail, dIndex) => (
                      <li key={dIndex} className="text-sm text-retro-dark-gray flex gap-2">
                        <span className="text-retro-blue">•</span>
                        <span>{detail}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
            <div className="mt-6 text-sm text-retro-brown">
              <p>📍 住所: 石川県金沢市八田町西1番地</p>
              <p className="mt-1">
                🌐 公式サイト:{' '}
                <a
                  href="https://www.keiba.go.jp/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-retro-blue underline"
                >
                  地方競馬全国協会（NAR）
                </a>
              </p>
            </div>
          </div>

          {/* 開催スケジュール */}
          <div className="newspaper-card p-8 mb-8 bg-retro-blue/10">
            <h2 className="text-2xl font-serif font-bold text-retro-brown mb-4">
              開催スケジュール
            </h2>
            <p className="text-sm text-retro-dark-gray mb-6">
              ※ 開催日は時期により変動します。詳細は公式サイトをご確認ください。
            </p>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
              {schedule.map((item, index) => (
                <div key={index} className="bg-white p-4 rounded-lg text-center">
                  <div className="font-bold text-retro-brown mb-2">{item.day}</div>
                  <div className="text-xs text-retro-dark-gray">{item.note}</div>
                </div>
              ))}
            </div>
            <div className="mt-6 text-sm text-retro-brown">
              <p>• 年間開催日数：約73日</p>
              <p>• 1日のレース数：通常10〜12レース</p>
              <p>• 第1レース発走：通常14:00頃</p>
            </div>
          </div>

          {/* 入場料・観覧料 */}
          <div className="newspaper-card p-8 mb-8">
            <h2 className="text-2xl font-serif font-bold text-retro-brown mb-4">
              入場料
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-lg">
                <div className="text-lg font-bold text-retro-brown mb-3">一般</div>
                <div className="text-4xl font-mono font-bold text-retro-green mb-2">
                  ¥100
                </div>
                <div className="text-sm text-retro-dark-gray">大人（20歳以上）</div>
              </div>
              <div className="bg-white p-6 rounded-lg">
                <div className="text-lg font-bold text-retro-brown mb-3">
                  中学生以下
                </div>
                <div className="text-4xl font-mono font-bold text-retro-blue mb-2">
                  無料
                </div>
                <div className="text-sm text-retro-dark-gray">家族で楽しめる</div>
              </div>
            </div>
            <div className="mt-4 text-sm text-retro-brown">
              ※ 入場料は時期により変動する場合があります。
            </div>
          </div>

          {/* 応援メッセージ */}
          <div className="newspaper-card p-8 md:p-10 text-center bg-gradient-to-br from-retro-crimson/10 to-retro-gold/10 border-2 border-retro-crimson">
            <h2 className="text-3xl font-serif font-bold text-retro-crimson mb-6">
              金沢競馬を応援しよう
            </h2>

            <div className="max-w-3xl mx-auto space-y-6">
              <p className="text-retro-dark-gray leading-relaxed">
                地方競馬は全国で廃止が相次いでいます。
                <br />
                金沢競馬場を未来に残すため、馬券購入で応援しましょう。
              </p>

              <div className="bg-white p-6 rounded-lg">
                <h3 className="text-xl font-bold text-retro-brown mb-4">
                  応援購入のススメ
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                  <div>
                    <div className="text-3xl mb-2">💰</div>
                    <div className="font-bold text-retro-brown mb-1">100円から</div>
                    <div className="text-retro-dark-gray">
                      少額から気軽に参加できる
                    </div>
                  </div>
                  <div>
                    <div className="text-3xl mb-2">🏇</div>
                    <div className="font-bold text-retro-brown mb-1">馬を支える</div>
                    <div className="text-retro-dark-gray">
                      売上は馬や騎手の活動資金に
                    </div>
                  </div>
                  <div>
                    <div className="text-3xl mb-2">❤️</div>
                    <div className="font-bold text-retro-brown mb-1">文化を守る</div>
                    <div className="text-retro-dark-gray">
                      地方競馬の文化を次世代へ
                    </div>
                  </div>
                </div>
              </div>

              <div className="text-sm text-retro-brown">
                ※ 全国どこからでも楽天競馬などのオンラインサービスで購入できます
              </div>

              <a
                href="https://keiba.rakuten.co.jp/"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block px-8 py-4 bg-retro-green text-white rounded-lg font-bold text-lg hover:bg-opacity-90 transition-colors shadow-retro"
              >
                楽天競馬で馬券を買う
              </a>

              <p className="text-xs text-retro-dark-gray mt-4">
                ※ 馬券購入は20歳以上の方に限ります
                <br />※ ギャンブル依存にご注意ください
              </p>
            </div>
          </div>

          {/* 金沢競馬の歴史 */}
          <div className="newspaper-card p-8 mb-8 mt-12">
            <h2 className="text-2xl font-serif font-bold text-retro-brown mb-6">
              金沢競馬の歴史
            </h2>
            <div className="space-y-4 text-sm text-retro-dark-gray leading-relaxed">
              <p>
                金沢競馬は、1952年（昭和27年）に開設された歴史ある地方競馬場です。
                北陸唯一の競馬場として、地域に根ざした運営を続けてきました。
              </p>
              <p>
                ダートコース1周1200mの小回りコースが特徴で、
                スピード勝負のレース展開が繰り広げられます。
                「北國王冠」などの重賞レースも開催され、全国から注目を集めています。
              </p>
              <p>
                2015年以降、売上の減少や施設の老朽化など厳しい状況が続いていますが、
                地元のファンや関係者の熱意に支えられ、今日まで続いています。
              </p>
              <p className="font-bold text-retro-crimson">
                この歴史と文化を未来に残すため、ぜひ金沢競馬を応援してください。
              </p>
            </div>
          </div>

          {/* データから見る金沢競馬 */}
          <div className="newspaper-card p-8 bg-retro-wheat/30">
            <h2 className="text-2xl font-serif font-bold text-retro-brown mb-6">
              データで見る金沢競馬（2015-2025年）
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-white p-4 rounded-lg text-center">
                <div className="text-sm text-retro-brown mb-2">総レース数</div>
                <div className="text-3xl font-bold font-mono text-retro-dark-gray">
                  8,718
                </div>
              </div>
              <div className="bg-white p-4 rounded-lg text-center">
                <div className="text-sm text-retro-brown mb-2">出走馬数</div>
                <div className="text-3xl font-bold font-mono text-retro-blue">
                  12,924
                </div>
              </div>
              <div className="bg-white p-4 rounded-lg text-center">
                <div className="text-sm text-retro-brown mb-2">騎手数</div>
                <div className="text-3xl font-bold font-mono text-retro-green">
                  281
                </div>
              </div>
              <div className="bg-white p-4 rounded-lg text-center">
                <div className="text-sm text-retro-brown mb-2">年間開催日</div>
                <div className="text-3xl font-bold font-mono text-retro-crimson">
                  約73日
                </div>
              </div>
            </div>
            <div className="mt-6 text-center">
              <a
                href="/stats"
                className="inline-block px-6 py-3 bg-retro-brown text-white rounded-lg font-bold hover:bg-opacity-90 transition-colors"
              >
                もっと詳しい統計を見る
              </a>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}
