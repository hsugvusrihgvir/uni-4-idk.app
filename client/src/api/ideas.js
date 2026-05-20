import { request } from './http.js'

export function createIdea(payload) {
  return request('/api/v1/ideas', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function getBoardIdeas(boardId) {
  return request(`/api/v1/boards/${boardId}/ideas`)
}

export function deleteIdea(ideaId) {
  return request(`/api/v1/ideas/${ideaId}`, {
    method: 'DELETE',
  })
}
