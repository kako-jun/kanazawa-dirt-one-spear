'use client'

import Image from 'next/image'
import Link from 'next/link'
import { useState } from 'react'

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <header className="showa-sign text-retro-wheat shadow-sign">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* ロゴエリア */}
        <div className="py-5 border-b-2 border-retro-gold-dark">
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
        <nav className="py-3">
          {/* デスクトップメニュー */}
          <div className="hidden md:flex items-center justify-center gap-1">
            {[
              { href: '/', label: 'ホーム' },
              { href: '/ai', label: 'AI予想' },
              { href: '/stats', label: '統計' },
              { href: '/racecourse', label: '競馬場' },
              { href: '/history', label: '履歴' },
            ].map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="px-5 py-2 font-bold text-retro-wheat hover:bg-retro-brown-light hover:text-retro-sepia rounded transition-colors border border-transparent hover:border-retro-gold-dark text-sm tracking-wide"
              >
                {item.label}
              </Link>
            ))}
          </div>

          {/* モバイルメニューボタン */}
          <div className="md:hidden flex justify-center">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="px-6 py-2 bg-retro-brown-light text-retro-wheat font-bold rounded border-2 border-retro-brown-dark text-sm"
              aria-label="メニューを開く"
            >
              {mobileMenuOpen ? '✕ 閉じる' : '☰ メニュー'}
            </button>
          </div>

          {/* モバイルメニュー */}
          {mobileMenuOpen && (
            <div className="md:hidden mt-3 flex flex-col gap-1 bg-retro-brown-dark rounded border-2 border-retro-brown p-3">
              {[
                { href: '/', label: 'ホーム' },
                { href: '/ai', label: 'AI予想' },
                { href: '/stats', label: '統計' },
                { href: '/racecourse', label: '競馬場' },
                { href: '/history', label: '履歴' },
              ].map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className="px-4 py-3 font-bold text-retro-wheat hover:bg-retro-brown hover:text-retro-sepia rounded transition-colors text-center text-sm"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {item.label}
                </Link>
              ))}
            </div>
          )}
        </nav>
      </div>
    </header>
  )
}
