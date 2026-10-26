import { apiFetch } from './api'

export interface Country {
  name: {
    common: string
    official: string
  }
  flags: {
    png: string
    alt?: string
  }
  capital?: string[]
  region: string
  population: number
  cca3: string
}

export async function getCountries(): Promise<Country[]> {
  const response = await apiFetch('/api/v1/integrations/countries')

  if (!response.ok) {
    throw new Error('Unable to load countries')
  }

  return response.json() as Promise<Country[]>
}
