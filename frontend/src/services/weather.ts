import { apiFetch } from './api'

export interface WeatherData {
  latitude: number
  longitude: number
  timezone: string
  current: {
    time: string
    temperature_2m: number
    relative_humidity_2m: number
    apparent_temperature: number
    is_day: number
    precipitation: number
    weather_code: number
    wind_speed_10m: number
  }
  condition: string
}

export async function getCurrentWeather(): Promise<WeatherData> {
  const response = await apiFetch(
    '/api/v1/integrations/weather/current?latitude=18.5204&longitude=73.8567',
  )

  if (!response.ok) {
    throw new Error('Unable to load weather data')
  }

  return response.json() as Promise<WeatherData>
}
