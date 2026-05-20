const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

let accessToken = localStorage.getItem('access_token') || ''

export function setAccessToken(token) {
  accessToken = token || ''

  if (accessToken) localStorage.setItem('access_token', accessToken)
  else localStorage.removeItem('access_token')
}

export async function request(path, options = {}) {
  const headers = {
    ...(options.body ? { 'Content-Type': 'application/json' } : {}),
    ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
    ...options.headers,
  }

  const response = await fetch(`${API_URL}${path}`, { ...options, headers })
  const data = response.status === 204 ? null : await response.json()

  if (!response.ok) {
    throw new Error(data?.detail || data?.message || 'Request failed')
  }

  return data
}
