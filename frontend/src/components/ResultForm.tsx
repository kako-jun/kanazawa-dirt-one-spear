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

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-yellow-600 text-white p-6 rounded-t-lg">
          <h2 className="text-2xl font-bold">レース結果を記録</h2>
          <p className="text-sm mt-1">{race.name} - 第{race.race_number}R</p>
        </div>

        <form onSubmit={handleSubmit} className="p-6">
          {/* 着順入力 */}
          <div className="mb-6">
            <h3 className="font-bold text-lg mb-3">着順</h3>
            <div className="grid grid-cols-3 gap-4">
              <div>
                <label className="block text-sm text-gray-600 mb-1">
                  1着
                </label>
                <select
                  value={first}
                  onChange={(e) => setFirst(parseInt(e.target.value))}
                  className="w-full p-3 border-2 border-gray-300 rounded-lg text-lg font-bold"
                  required
                >
                  {race.entries.map((entry) => (
                    <option key={entry.horse_number} value={entry.horse_number}>
                      {entry.horse_number}番 {entry.horse.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm text-gray-600 mb-1">
                  2着
                </label>
                <select
                  value={second}
                  onChange={(e) => setSecond(parseInt(e.target.value))}
                  className="w-full p-3 border-2 border-gray-300 rounded-lg text-lg font-bold"
                  required
                >
                  {race.entries.map((entry) => (
                    <option key={entry.horse_number} value={entry.horse_number}>
                      {entry.horse_number}番 {entry.horse.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm text-gray-600 mb-1">
                  3着
                </label>
                <select
                  value={third}
                  onChange={(e) => setThird(parseInt(e.target.value))}
                  className="w-full p-3 border-2 border-gray-300 rounded-lg text-lg font-bold"
                  required
                >
                  {race.entries.map((entry) => (
                    <option key={entry.horse_number} value={entry.horse_number}>
                      {entry.horse_number}番 {entry.horse.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* 3連単配当 */}
          <div className="mb-6">
            <label className="block font-bold text-lg mb-2">
              3連単配当（100円あたり）
            </label>
            <input
              type="number"
              value={payout}
              onChange={(e) => setPayout(e.target.value)}
              placeholder="例: 12340"
              className="w-full p-3 border-2 border-gray-300 rounded-lg"
            />
            <p className="text-sm text-gray-500 mt-1">
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
                className="w-6 h-6"
              />
              <span className="font-bold text-lg">実際に購入した</span>
            </label>
          </div>

          {/* 購入金額（購入した場合のみ） */}
          {purchased && (
            <div className="mb-6 ml-9">
              <label className="block font-bold mb-2">購入金額（円）</label>
              <input
                type="number"
                value={betAmount}
                onChange={(e) => setBetAmount(e.target.value)}
                placeholder="例: 100"
                className="w-full p-3 border-2 border-gray-300 rounded-lg"
                required
              />
            </div>
          )}

          {/* メモ */}
          <div className="mb-6">
            <label className="block font-bold text-lg mb-2">
              メモ・感想（任意）
            </label>
            <textarea
              value={memo}
              onChange={(e) => setMemo(e.target.value)}
              placeholder="レースの感想や反省点など"
              rows={3}
              className="w-full p-3 border-2 border-gray-300 rounded-lg"
            />
          </div>

          {/* ボタン */}
          <div className="flex gap-4">
            <button
              type="button"
              onClick={onCancel}
              className="flex-1 px-6 py-3 bg-gray-300 text-gray-700 rounded-lg font-bold hover:bg-gray-400 transition-colors"
              disabled={submitting}
            >
              キャンセル
            </button>
            <button
              type="submit"
              className="flex-1 px-6 py-3 bg-yellow-600 text-white rounded-lg font-bold hover:bg-yellow-700 transition-colors disabled:bg-gray-400"
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
