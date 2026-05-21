import { API_URL, request } from './http.js'

export function checkUsername(username) {
  return request(`/api/v1/users/check-username?username=${encodeURIComponent(username)}`)
}

export function getMe() {
  return request('/api/v1/users/me')
}

export function updateMe(data) {
  return request('/api/v1/users/me', {
    method: 'PATCH',
    body: JSON.stringify(data),
  })
}

export function uploadAvatar(file) {
  const data = new FormData()
  data.append('file', file)

  return request('/api/v1/users/avatar', {
    method: 'POST',
    body: data,
  })
}

export function fileUrl(url) {
  return url?.startsWith('/uploads') ? `${API_URL}${url}` : url
}
