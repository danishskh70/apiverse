import { apiFetch } from './api'
export interface ApodResponse {
  date: string
  title: string
  explanation: string
  url: string
  hdurl?: string
  media_type: 'image' | 'video' | string
  service_version?: string
  copyright?: string
}

export async function getApod(date?: string): Promise<ApodResponse> {
  const params = new URLSearchParams()

  if (date) {
    params.set('date', date)
  }

  const query = params.toString()
  const endpoint = `/api/v1/integrations/space/apod${query ? `?${query}` : ''}`

  const response = await apiFetch(endpoint)

  if (!response.ok) {
    if (response.status === 429) {
      throw new Error('NASA API rate limit reached. Try again later.')
    }

    throw new Error('Unable to load NASA astronomy data right now.')
  }

  return response.json() as Promise<ApodResponse>
}
