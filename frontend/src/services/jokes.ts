import { apiFetch } from './api'
export interface JokeResponse {
  error: boolean
  category: string
  type: 'single' | 'twopart'
  joke?: string
  setup?: string
  delivery?: string
  safe: boolean
}

export async function getRandomJoke(): Promise<JokeResponse> {
  const response = await apiFetch('/api/v1/integrations/jokebox/random')

  if (!response.ok) {
    if (response.status === 429) {
      throw new Error('Too many requests. Please try again later.')
    }

    throw new Error('Unable to load a joke right now.')
  }

  return response.json() as Promise<JokeResponse>
}
