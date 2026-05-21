export const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

let accessToken = localStorage.getItem('access_token') || ''

export function setAccessToken(token) {
  accessToken = token || ''

  if (accessToken) localStorage.setItem('access_token', accessToken)
  else localStorage.removeItem('access_token')
}

export async function request(path, options = {}) {
  const isForm = options.body instanceof FormData
  const headers = {
    ...(options.body && !isForm ? { 'Content-Type': 'application/json' } : {}),
    ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
    ...options.headers,
  }

  let response

  try {
    response = await fetch(`${API_URL}${path}`, { ...options, headers })
  } catch {
    throw new Error('Сейчас не получается связаться с сервисом. Попробуйте еще раз чуть позже.')
  }

  const data = response.status === 204 ? null : await response.json().catch(() => null)

  if (!response.ok) {
    throw new Error(data?.detail || data?.message || 'Ошибка запроса')
  }

  return data
}
