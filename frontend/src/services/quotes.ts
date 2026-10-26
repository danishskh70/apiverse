export interface DailyQuote {
  quote: string
  author: string
  source: string
}

export async function getDailyQuote(): Promise<DailyQuote> {
  const response = await fetch('/api/v1/integrations/quotes/daily')

  if (!response.ok) {
    throw new Error("Unable to load today's quote. Please try again later.")
  }

  return response.json() as Promise<DailyQuote>
}
