const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface Horse {
  horse_id: string
  name: string
  age: number
  gender: string
}

export interface Entry {
  entry_id: string
  race_id: string
  horse: Horse
  gate_number: number
  horse_number: number
  jockey: string
  weight: number
  odds?: number
  past_results?: number[]
}

export interface Race {
  race_id: string
  date: string
  race_number: number
  name: string
  distance: number
  track_condition: string
  weather: string
  entries: Entry[]
}

export interface Prediction {
  prediction_id: string
  race_id: string
  predicted_at: string
  first: number
  second: number
  third: number
  confidence: number
  model_version: string
}

export interface Result {
  result_id: string
  race_id: string
  first: number
  second: number
  third: number
  payout_trifecta?: number
  prediction_hit: boolean
  purchased: boolean
  bet_amount?: number
  return_amount?: number
  recorded_at: string
  memo?: string
}

export interface ResultSubmit {
  race_id: string
  first: number
  second: number
  third: number
  payout_trifecta?: number
  purchased: boolean
  bet_amount?: number
  memo?: string
}

export interface Statistics {
  total_races: number
  total_predictions: number
  hit_count: number
  hit_rate: number
  purchased_count: number
  purchased_hit_count: number
  purchased_hit_rate: number
  roi: number
  total_investment: number
  total_return: number
  profit: number
  max_payout: number
  recent_results: string[]
}

export const apiClient = {
  async getRaces(date?: string): Promise<Race[]> {
    const url = date
      ? `${API_BASE_URL}/api/races?date=${date}`
      : `${API_BASE_URL}/api/races`
    const response = await fetch(url)
    if (!response.ok) throw new Error('Failed to fetch races')
    return response.json()
  },

  async getRace(raceId: string): Promise<Race> {
    const response = await fetch(`${API_BASE_URL}/api/races/${raceId}`)
    if (!response.ok) throw new Error('Failed to fetch race')
    return response.json()
  },

  async getPrediction(raceId: string): Promise<Prediction> {
    const response = await fetch(`${API_BASE_URL}/api/predictions/${raceId}`)
    if (!response.ok) throw new Error('Failed to fetch prediction')
    return response.json()
  },

  async getStatistics(): Promise<Statistics> {
    const response = await fetch(`${API_BASE_URL}/api/stats`)
    if (!response.ok) throw new Error('Failed to fetch statistics')
    return response.json()
  },

  async getResults(): Promise<Result[]> {
    const response = await fetch(`${API_BASE_URL}/api/results`)
    if (!response.ok) throw new Error('Failed to fetch results')
    return response.json()
  },

  async submitResult(result: ResultSubmit): Promise<Result> {
    const response = await fetch(`${API_BASE_URL}/api/results`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(result),
    })
    if (!response.ok) throw new Error('Failed to submit result')
    return response.json()
  },
}
