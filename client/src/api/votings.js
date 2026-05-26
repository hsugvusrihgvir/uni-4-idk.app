import { request } from './http.js'

export function createVoting(boardId, data) {
  return request(`/api/v1/boards/${boardId}/votings`, {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function getVotings(boardId) {
  return request(`/api/v1/boards/${boardId}/votings`)
}

export function deleteVoting(votingId) {
  return request(`/api/v1/votings/${votingId}`, {
    method: 'DELETE',
  })
}

export function createVote(data) {
  return request('/api/v1/votes', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function deleteVote(data) {
  return request('/api/v1/votes', {
    method: 'DELETE',
    body: JSON.stringify(data),
  })
}

export function getVotingResults(votingId) {
  return request(`/api/v1/votings/${votingId}/results`)
}
