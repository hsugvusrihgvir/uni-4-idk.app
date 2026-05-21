import { request } from './http.js'

export function login(email) {
  return request('/api/v1/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email }),
  })
}

export function register(data) {
  return request('/api/v1/auth/register', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function verify(data) {
  return request('/api/v1/auth/verify', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function refresh(refreshToken) {
  return request('/api/v1/auth/refresh', {
    method: 'POST',
    body: JSON.stringify({ refresh_token: refreshToken }),
  })
}
