'use client'

import { useState } from 'react'
import { Race, ResultSubmit, apiClient } from '@/lib/api-client'

interface ResultFormProps {
  race: Race
  onSubmitted: () => void
  onCancel: () => void
}

export default function ResultForm({
  race,
  onSubmitted,
  onCancel,
}: ResultFormProps) {
  const [first, setFirst] = useState<number>(1)
  const [second, setSecond] = useState<number>(2)
  const [third, setThird] = useState<number>(3)
  const [payout, setPayout] = useState<string>('')
  const [purchased, setPurchased] = useState<boolean>(false)
  const [betAmount, setBetAmount] = useState<string>('')
  const [memo, setMemo] = useState<string>('')
  const [submitting, setSubmitting] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    try {
      setSubmitting(true)

      const result: ResultSubmit = {
        race_id: race.race_id,
        first,
        second,
        third,
        payout_trifecta: payout ? parseInt(payout) : undefined,
        purchased,
        bet_amount: purchased && betAmount ? parseInt(betAmount) : undefined,
        memo: memo || undefined,
      }

      await apiClient.submitResult(result)
      onSubmitted()
    } catch (error) {
      console.error('Failed to submit result:', error)
      alert('結果の登録に失敗しました')
    } finally {
      setSubmitting(false)
    }
  }

  const inputClass = "w-full p-3 border-2 border-retro-brown rounded-sm bg-retro-sepia text-retro-brown-dark font-mono focus:outline-none focus:border-retro-gold"
  const selectClass = "w-full p-3 border-2 border-retro-brown rounded-sm bg-retro-sepia text-retro-brown-dark text-base font-bold font-mono focus:outline-none focus:border-retro-gold"
  const labelClass = "block text-xs text-retro-brown font-bold font-mono mb-1"

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center p-4 z-50">
      <div
        className="max-w-2xl w-full max-h-[90vh] overflow-y-auto rounded-sm"
        style={{
          background: '#EDE0C4',
          border: '3px solid #3D1C0E',
          borderBottom: '6px solid #2A1008',
          boxShadow: '8px 8px 0 rgba(0,0,0,0.5)'
        }}
      >
        {/* ヘッダー看板 */}
        <div className="sticky top-0 showa-sign p-5 rounded-t-sm">
          <h2
            className="text-xl font-serif font-black text-retro-wheat"
            style={{ textShadow: '2px 2px 4px rgba(0,0,0,0.7)' }}
          >
            レース結果を記録
          </h2>
          <p className="text-xs text-retro-wheat opacity-70 mt-1 font-mono">
            {race.name} — 第{race.race_number}R
          </p>
        </div>

        <form onSubmit={handleSubmit} className="p-6">
          {/* 着順入力 */}
          <div className="mb-6">
            <h3 className="font-serif font-black text-retro-brown-dark text-base mb-3">着順</h3>
            <div className="grid grid-cols-3 gap-4">
              {[
                { label: '1着', value: first, setter: setFirst },
                { label: '2着', value: second, setter: setSecond },
                { label: '3着', value: third, setter: setThird },
              ].map(({ label, value, setter }) => (
                <div key={label}>
                  <label className={labelClass}>{label}</label>
                  <select
                    value={value}
                    onChange={(e) => setter(parseInt(e.target.value))}
                    className={selectClass}
                    required
                  >
                    {race.entries.map((entry) => (
                      <option key={entry.horse_number} value={entry.horse_number}>
                        {entry.horse_number}番 {entry.horse.name}
                      </option>
                    ))}
                  </select>
                </div>
              ))}
            </div>
          </div>

          {/* 3連単配当 */}
          <div className="mb-6">
            <label className="block font-serif font-black text-retro-brown-dark text-base mb-2">
              三連単配当（100円あたり）
            </label>
            <input
              type="number"
              value={payout}
              onChange={(e) => setPayout(e.target.value)}
              placeholder="例: 12340"
              className={inputClass}
            />
            <p className="text-xs text-retro-brown opacity-60 mt-1 font-mono">
              ※配当がわかる場合は入力してください
            </p>
          </div>

          {/* 購入有無 */}
          <div className="mb-6">
            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={purchased}
                onChange={(e) => setPurchased(e.target.checked)}
                className="w-5 h-5 accent-retro-crimson"
              />
              <span className="font-serif font-bold text-retro-brown-dark">実際に購入した</span>
            </label>
          </div>

          {/* 購入金額 */}
          {purchased && (
            <div className="mb-6 ml-8">
              <label className="block font-bold text-retro-brown-dark mb-2 font-serif">購入金額（円）</label>
              <input
                type="number"
                value={betAmount}
                onChange={(e) => setBetAmount(e.target.value)}
                placeholder="例: 100"
                className={inputClass}
                required
              />
            </div>
          )}

          {/* メモ */}
          <div className="mb-6">
            <label className="block font-serif font-black text-retro-brown-dark text-base mb-2">
              メモ・感想（任意）
            </label>
            <textarea
              value={memo}
              onChange={(e) => setMemo(e.target.value)}
              placeholder="レースの感想や反省点など"
              rows={3}
              className={inputClass}
            />
          </div>

          {/* ボタン */}
          <div className="flex gap-4">
            <button
              type="button"
              onClick={onCancel}
              className="flex-1 px-6 py-3 font-bold rounded-sm transition-colors text-retro-wheat border-2 border-retro-dark-gray"
              style={{
                background: 'linear-gradient(180deg, #3A4E4C 0%, #2A3A38 100%)',
                boxShadow: '2px 2px 0 rgba(0,0,0,0.3)'
              }}
              disabled={submitting}
            >
              キャンセル
            </button>
            <button
              type="submit"
              className="flex-1 px-6 py-3 font-black rounded-sm transition-colors text-retro-wheat border-2 border-retro-brown-dark disabled:opacity-50"
              style={{
                background: 'linear-gradient(180deg, #C9920A 0%, #8B6500 100%)',
                boxShadow: '2px 2px 0 rgba(0,0,0,0.3)',
                textShadow: '1px 1px 2px rgba(0,0,0,0.5)'
              }}
              disabled={submitting}
            >
              {submitting ? '登録中...' : '登録する'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
