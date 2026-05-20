import { request } from './http.js'

export function login(email) {
  return request('/api/v1/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email }),
  })
}

export function register(payload) {
  return request('/api/v1/auth/register', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function verify(payload) {
  return request('/api/v1/auth/verify', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function refresh(refreshToken) {
  return request('/api/v1/auth/refresh', {
    method: 'POST',
    body: JSON.stringify({ refresh_token: refreshToken }),
  })
}
