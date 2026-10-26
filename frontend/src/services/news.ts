import { apiFetch } from './api'

export type NewsCategory =
  | 'general'
  | 'business'
  | 'entertainment'
  | 'health'
  | 'science'
  | 'sports'
  | 'technology'

export interface NewsArticle {
  source: {
    id: string | null
    name: string
  }
  author?: string | null
  title: string
  description?: string | null
  url: string
  urlToImage?: string | null
  publishedAt: string
  content?: string | null
}

export interface NewsResponse {
  totalResults: number
  articles: NewsArticle[]
}

export async function getTopHeadlines(
  category: NewsCategory = 'general',
  q?: string,
): Promise<NewsResponse> {
  const params = new URLSearchParams({
    country: 'in',
    category,
    page_size: '12',
  })

  if (q?.trim()) {
    params.set('q', q.trim())
  }

  const response = await apiFetch(
    `/api/v1/integrations/news?${params.toString()}`,
  )

  if (!response.ok) {
    throw new Error('Unable to load news right now.')
  }

  return response.json() as Promise<NewsResponse>
}
