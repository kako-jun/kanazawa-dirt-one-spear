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
        // レトロカラーパレット（昭和競馬場イメージ）- 深化版
        retro: {
          // ダートコース系 — より濃く、本物の土の色
          brown: '#6B3A2A',           // 焼けた木材、古い看板の枠
          'brown-light': '#8B5E3C',   // 昼間の土、明るい板材
          'brown-dark': '#3D1C0E',    // 夜の木材、影
          // コンクリート・建物系
          'dark-gray': '#2A3A38',     // 古いコンクリートスタンド
          'slate': '#1C2B28',         // 夜の競馬場、夕暮れ後
          // 紙・壁系
          wheat: '#E8C99A',           // 古びた壁紙、馬券の紙
          'wheat-dark': '#C9A87A',    // 汚れた紙、日焼けした壁
          sepia: '#F2E8D5',           // 新聞紙、セピア写真
          'sepia-dark': '#DDD0B8',    // 古い新聞、経年変化した紙
          parchment: '#EDE0C4',       // 羊皮紙風、馬券の台紙
          // アクセント系
          crimson: '#C8102E',         // 勝負の赤、的中スタンプ
          'crimson-dark': '#8B0000',  // 深紅、ボタン枠
          scarlet: '#D42B2B',         // 看板の赤文字
          gold: '#C9920A',            // くすんだ金、配当表示
          'gold-bright': '#E8A900',   // 明るい金
          'gold-dark': '#8B6500',     // 暗い金
          // データ系（青）
          blue: '#2C5F8A',            // データ、AI — より渋く
          'blue-light': '#4A7FA5',    // 明るいデータ表示
          // 芝・緑
          green: '#2E6B2E',           // 芝生（濃く、本物らしく）
          // chalk（チョーク文字）
          chalk: '#F5F0E8',           // 黒板のチョーク
          // 木炭・木材
          charcoal: '#2C2C2C',        // チョーク黒板
          'wood-dark': '#4A2C1A',     // 古い木材
          // 赤茶（馬体色）
          'dirt-light': '#B87D5A',    // 軽い砂埃
          'dirt-mid': '#9B6543',      // ダート中間色
          'dirt-deep': '#7A4A2E',     // 深いダート
        },
      },
      fontFamily: {
        'serif': ['Noto Serif JP', 'serif'],
        'sans': ['Noto Sans JP', 'sans-serif'],
        'mono': ['Courier New', 'Roboto Mono', 'monospace'],
      },
      boxShadow: {
        // 昭和看板の影
        'retro': '4px 4px 0 rgba(0,0,0,0.35)',
        'retro-lg': '6px 6px 0 rgba(0,0,0,0.35)',
        'retro-inset': 'inset 2px 2px 0 rgba(0,0,0,0.2)',
        // スタンプ風
        'stamp': '3px 3px 0 rgba(0,0,0,0.4)',
        // LED/電光掲示板
        'led': 'inset 0 0 12px rgba(201,146,10,0.4), inset 0 0 4px rgba(201,146,10,0.2)',
        'led-bright': 'inset 0 0 20px rgba(201,146,10,0.6), 0 0 8px rgba(201,146,10,0.3)',
        // 看板風
        'sign': '5px 5px 0 rgba(61,28,14,0.5)',
        'sign-sm': '3px 3px 0 rgba(61,28,14,0.5)',
        // 馬券カード
        'ticket': '2px 2px 8px rgba(0,0,0,0.25), inset 0 0 0 1px rgba(0,0,0,0.1)',
        // 木の板
        'board': '4px 4px 0 rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.1)',
      },
      backgroundImage: {
        // 古びた紙テクスチャ（CSS グラデーションで疑似的に）
        'aged-paper': 'repeating-linear-gradient(45deg, transparent, transparent 2px, rgba(0,0,0,0.015) 2px, rgba(0,0,0,0.015) 4px)',
        'aged-paper-dark': 'repeating-linear-gradient(45deg, transparent, transparent 2px, rgba(0,0,0,0.03) 2px, rgba(0,0,0,0.03) 4px)',
        // ダート（砂利）テクスチャ
        'dirt-texture': 'radial-gradient(ellipse at 20% 30%, rgba(184,125,90,0.3) 0%, transparent 50%), radial-gradient(ellipse at 80% 70%, rgba(107,58,42,0.2) 0%, transparent 50%)',
        // 木目テクスチャ
        'wood-grain': 'repeating-linear-gradient(90deg, transparent, transparent 8px, rgba(0,0,0,0.03) 8px, rgba(0,0,0,0.03) 9px)',
        // 黒板
        'blackboard': 'linear-gradient(135deg, #2C2C2C 0%, #1A1A1A 100%)',
        // 昭和看板グラデーション
        'showa-header': 'linear-gradient(180deg, #3D1C0E 0%, #6B3A2A 40%, #5A2D1A 100%)',
        // ダートコース
        'dirt-course': 'linear-gradient(180deg, #B87D5A 0%, #9B6543 40%, #7A4A2E 100%)',
      },
      borderWidth: {
        '3': '3px',
        '5': '5px',
        '6': '6px',
      },
      spacing: {
        '18': '4.5rem',
        '22': '5.5rem',
      },
      animation: {
        'flicker': 'flicker 3s infinite',
        'stamp-appear': 'stampAppear 0.3s ease-out',
      },
      keyframes: {
        flicker: {
          '0%, 100%': { opacity: '1' },
          '92%': { opacity: '0.95' },
          '94%': { opacity: '0.85' },
          '96%': { opacity: '0.95' },
        },
        stampAppear: {
          '0%': { transform: 'rotate(-15deg) scale(1.5)', opacity: '0' },
          '100%': { transform: 'rotate(-15deg) scale(1)', opacity: '0.9' },
        },
      },
    },
  },
  plugins: [],
}
