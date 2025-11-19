'use client'

import Image from 'next/image'
import Link from 'next/link'
import { useState } from 'react'

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <header className="bg-retro-brown text-retro-sepia shadow-retro">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* ロゴエリア */}
        <div className="py-6 border-b-2 border-retro-wheat">
          <Link href="/" className="block">
            <div className="flex flex-col items-center gap-2">
              <Image
                src="/images/kanazawa-dart-logo.webp"
                alt="金沢ダート一本槍 Kanazawa Dart 1 Spear"
                width={900}
                height={173}
                priority
                className="max-w-[900px] w-full h-auto drop-shadow-md"
                sizes="(max-width: 640px) 90vw, (max-width: 1024px) 720px, 900px"
              />
              <p className="sr-only">AIが選ぶ三連単一点予想</p>
            </div>
          </Link>
        </div>

        {/* ナビゲーション */}
        <nav className="py-4">
          {/* デスクトップメニュー */}
          <div className="hidden md:flex items-center justify-center gap-6">
            <Link
              href="/"
              className="px-4 py-2 font-bold hover:bg-retro-wheat hover:text-retro-brown rounded transition-colors"
            >
              ホーム
            </Link>
            <Link
              href="/ai"
              className="px-4 py-2 font-bold hover:bg-retro-wheat hover:text-retro-brown rounded transition-colors"
            >
              AI予想
            </Link>
            <Link
              href="/stats"
              className="px-4 py-2 font-bold hover:bg-retro-wheat hover:text-retro-brown rounded transition-colors"
            >
              統計
            </Link>
            <Link
              href="/racecourse"
              className="px-4 py-2 font-bold hover:bg-retro-wheat hover:text-retro-brown rounded transition-colors"
            >
              競馬場
            </Link>
            <Link
              href="/history"
              className="px-4 py-2 font-bold hover:bg-retro-wheat hover:text-retro-brown rounded transition-colors"
            >
              履歴
            </Link>
          </div>

          {/* モバイルメニューボタン */}
          <div className="md:hidden flex justify-center">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="px-4 py-2 bg-retro-wheat text-retro-brown font-bold rounded"
              aria-label="メニューを開く"
            >
              {mobileMenuOpen ? '✕ 閉じる' : '☰ メニュー'}
            </button>
          </div>

          {/* モバイルメニュー */}
          {mobileMenuOpen && (
            <div className="md:hidden mt-4 flex flex-col gap-2 bg-retro-wheat rounded-lg p-4">
              <Link
                href="/"
                className="px-4 py-3 font-bold text-retro-brown hover:bg-retro-brown hover:text-retro-sepia rounded transition-colors text-center"
                onClick={() => setMobileMenuOpen(false)}
              >
                ホーム
              </Link>
              <Link
                href="/ai"
                className="px-4 py-3 font-bold text-retro-brown hover:bg-retro-brown hover:text-retro-sepia rounded transition-colors text-center"
                onClick={() => setMobileMenuOpen(false)}
              >
                AI予想
              </Link>
              <Link
                href="/stats"
                className="px-4 py-3 font-bold text-retro-brown hover:bg-retro-brown hover:text-retro-sepia rounded transition-colors text-center"
                onClick={() => setMobileMenuOpen(false)}
              >
                統計
              </Link>
              <Link
                href="/racecourse"
                className="px-4 py-3 font-bold text-retro-brown hover:bg-retro-brown hover:text-retro-sepia rounded transition-colors text-center"
                onClick={() => setMobileMenuOpen(false)}
              >
                競馬場
              </Link>
              <Link
                href="/history"
                className="px-4 py-3 font-bold text-retro-brown hover:bg-retro-brown hover:text-retro-sepia rounded transition-colors text-center"
                onClick={() => setMobileMenuOpen(false)}
              >
                履歴
              </Link>
            </div>
          )}
        </nav>
      </div>
    </header>
  )
}
