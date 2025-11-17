/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: 'var(--background)',
        foreground: 'var(--foreground)',
        // レトロカラーパレット（昭和競馬場イメージ）
        retro: {
          brown: '#8B4513',        // ダートコース、古びた木材
          'dark-gray': '#2F4F4F',  // コンクリート、古いトンネル
          wheat: '#F5DEB3',        // 古びた壁、セピア写真
          green: '#228B22',        // 公園の芝生
          crimson: '#DC143C',      // 勝負の赤、的中表示
          gold: '#FFD700',         // 配当、勝利
          blue: '#4169E1',         // データ、AI
          sepia: '#FFF8DC',        // セピアトーン背景
          'dark-red': '#8B0000',   // ボタン枠線
        },
      },
      fontFamily: {
        'serif': ['Noto Serif JP', 'serif'],      // 見出し用明朝体
        'sans': ['Noto Sans JP', 'sans-serif'],   // 本文用ゴシック体
        'mono': ['Courier New', 'Roboto Mono', 'monospace'], // 数字用
      },
      boxShadow: {
        'retro': '5px 5px 10px rgba(0,0,0,0.2)',
        'stamp': '3px 3px 0 rgba(0,0,0,0.3)',
        'led': 'inset 0 0 10px rgba(255,215,0,0.3)',
      },
    },
  },
  plugins: [],
}
