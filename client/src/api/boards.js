import { request } from './http.js'

export function createBoard(payload) {
  return request('/api/v1/boards', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function getBoards() {
  return request('/api/v1/boards')
}

export function getBoard(boardId) {
  return request(`/api/v1/boards/${boardId}`)
}

export function deleteBoard(boardId) {
  return request(`/api/v1/boards/${boardId}`, {
    method: 'DELETE',
  })
}
