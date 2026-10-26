const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? '').replace(/\/$/, '')

export function apiFetch(
  input: RequestInfo | URL,
  init?: RequestInit,
): Promise<Response> {
  const path = String(input)

  const url = API_BASE_URL
    ? `${API_BASE_URL}${path.startsWith('/') ? path : `/${path}`}`
    : path

  return fetch(url, init)
}
