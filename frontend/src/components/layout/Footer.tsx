export default function Footer() {
  return (
    <footer className="bg-retro-slate text-retro-wheat mt-20 border-t-4 border-retro-brown-dark">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 免責事項 */}
        <div className="text-center mb-6 space-y-2">
          <p className="text-sm opacity-80">
            本サイトは非営利・研究目的で運営しています
          </p>
          <p className="text-sm opacity-80">
            データ出典: ©地方競馬全国協会（NAR）
          </p>
          <p className="text-sm">
            <a
              href="https://www.keiba.go.jp/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-retro-gold-bright hover:underline"
            >
              NAR公式サイト
            </a>
          </p>
        </div>

        {/* 注意書き */}
        <div className="border-t-2 border-retro-brown pt-6 text-center space-y-2">
          <p className="text-xs opacity-60">
            ※予想は必ず当たるものではありません。参考情報としてご覧ください。
          </p>
          <p className="text-xs opacity-60">
            ギャンブル依存に注意し、余剰資金の範囲で楽しみましょう。
          </p>
          <p className="text-xs opacity-60">
            20歳未満の方は馬券を購入できません。
          </p>
        </div>

        {/* コピーライト */}
        <div className="mt-6 text-center">
          <p className="text-xs opacity-40 font-mono tracking-wide">
            © 2025 金沢ダート一本槍 All Rights Reserved.
          </p>
        </div>
      </div>
    </footer>
  )
}
