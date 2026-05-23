export const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

let accessToken = localStorage.getItem('access_token') || ''
let refreshPromise = null
let sessionExpiredHandler = null
let tokenRefreshedHandler = null

export function setAccessToken(token) {
  accessToken = token || ''

  if (accessToken) localStorage.setItem('access_token', accessToken)
  else localStorage.removeItem('access_token')
}

export function setAuthSessionHandlers({ onRefresh, onExpired } = {}) {
  tokenRefreshedHandler = onRefresh || null
  sessionExpiredHandler = onExpired || null
}

function getRefreshToken() {
  return localStorage.getItem('refresh_token') || ''
}

function clearAuthTokens() {
  accessToken = ''
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
}

function makeHeaders(options) {
  const isForm = options.body instanceof FormData

  return {
    ...(options.body && !isForm ? { 'Content-Type': 'application/json' } : {}),
    ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
    ...options.headers,
  }
}

async function parseResponse(response) {
  const data = response.status === 204 ? null : await response.json().catch(() => null)

  if (!response.ok) {
    throw new Error(data?.detail || data?.message || 'Ошибка запроса')
  }

  return data
}

async function fetchRequest(path, options) {
  return fetch(`${API_URL}${path}`, { ...options, headers: makeHeaders(options) })
}

async function refreshAccessToken() {
  if (!refreshPromise) {
    refreshPromise = (async () => {
      const refreshToken = getRefreshToken()
      if (!refreshToken) throw new Error('Session expired')

      const response = await fetch(`${API_URL}/api/v1/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: refreshToken }),
      })
      const data = response.status === 204 ? null : await response.json().catch(() => null)

      if (!response.ok || !data?.access_token) {
        clearAuthTokens()
        sessionExpiredHandler?.()
        throw new Error(data?.detail || 'Session expired')
      }

      setAccessToken(data.access_token)
      tokenRefreshedHandler?.(data.access_token)
      return data.access_token
    })().finally(() => {
      refreshPromise = null
    })
  }

  return refreshPromise
}

export async function request(path, options = {}) {
  const { skipAuthRefresh, ...fetchOptions } = options
  let response

  try {
    response = await fetchRequest(path, fetchOptions)
  } catch {
    throw new Error('Сейчас не получается связаться с сервисом. Попробуйте еще раз чуть позже.')
  }

  if (response.status === 401 && !skipAuthRefresh && path !== '/api/v1/auth/refresh' && getRefreshToken()) {
    await refreshAccessToken()
    response = await fetchRequest(path, fetchOptions)
  }

  return parseResponse(response)
}
