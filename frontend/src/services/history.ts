import { apiFetch } from './api'
export interface HistoricalEvent {
  year: number
  title: string
  pages: {
    title: string
    url?: string
  }[]
}

export interface HistoryResponse {
  date: string
  events: HistoricalEvent[]
  source: string
}

export async function getHistoricalEvents(): Promise<HistoryResponse> {
  const response = await apiFetch('/api/v1/integrations/history/today')

  if (!response.ok) {
    throw new Error('Unable to load historical events. Please try again later.')
  }

  return response.json() as Promise<HistoryResponse>
}