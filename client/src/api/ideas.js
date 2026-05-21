import { request } from './http.js'

export function createIdea(data) {
  return request('/api/v1/ideas', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function getBoardIdeas(boardId) {
  return request(`/api/v1/boards/${boardId}/ideas`)
}

export function getModerationIdeas(boardId) {
  return request(`/api/v1/boards/${boardId}/ideas/moderation`)
}

export function updateIdeaStatus(ideaId, data) {
  return request(`/api/v1/ideas/${ideaId}/status`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  })
}

export function deleteIdea(ideaId) {
  return request(`/api/v1/ideas/${ideaId}`, {
    method: 'DELETE',
  })
}

export function getIdeasWsUrl(boardId, token) {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  const apiUrl = new URL(import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000')

  return `${protocol}//${apiUrl.host}/api/v1/boards/${boardId}/ideas/ws?token=${encodeURIComponent(token)}`
}
