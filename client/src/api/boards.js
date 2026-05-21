import { request } from './http.js'

export function createBoard(data) {
  return request('/api/v1/boards', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function getBoards() {
  return request('/api/v1/boards')
}

export function getBoard(boardId) {
  return request(`/api/v1/boards/${boardId}`)
}

export function updateBoard(boardId, data) {
  return request(`/api/v1/boards/${boardId}`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  })
}

export function deleteBoard(boardId) {
  return request(`/api/v1/boards/${boardId}`, {
    method: 'DELETE',
  })
}

export function getMembers(boardId) {
  return request(`/api/v1/boards/${boardId}/members`)
}

export function addMember(boardId, data) {
  return request(`/api/v1/boards/${boardId}/members`, {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function updateMemberRole(boardId, userId, data) {
  return request(`/api/v1/boards/${boardId}/members/${userId}/role`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  })
}

export function deleteMember(boardId, userId) {
  return request(`/api/v1/boards/${boardId}/members/${userId}`, {
    method: 'DELETE',
  })
}
