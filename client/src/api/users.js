import { request } from './http.js'

export function checkUsername(username) {
  return request(`/api/v1/users/check-username?username=${encodeURIComponent(username)}`)
}

export function getMe() {
  return request('/api/v1/users/me')
}

export function updateMe(payload) {
  return request('/api/v1/users/me', {
    method: 'PATCH',
    body: JSON.stringify(payload),
  })
}
