import { computed, reactive } from 'vue'
import { defaultState } from './defaultState.js'
import { saveTokens, clearTokens } from '../utils/storage.js'
import { setAccessToken } from '../api/http.js'
import * as authApi from '../api/auth.js'
import * as usersApi from '../api/users.js'
import * as boardsApi from '../api/boards.js'
import * as ideasApi from '../api/ideas.js'
import { notReady } from '../api/stubs.js'

const state = reactive(structuredClone(defaultState))
setAccessToken(state.auth.accessToken)

const text = {
  anonymous: '\u0430\u043d\u043e\u043d\u0438\u043c\u043d\u043e',
  member: '\u0443\u0447\u0430\u0441\u0442\u043d\u0438\u043a',
  requestError: '\u041e\u0448\u0438\u0431\u043a\u0430 \u0437\u0430\u043f\u0440\u043e\u0441\u0430',
  rejectReason: '\u041f\u0440\u0438\u0447\u0438\u043d\u0430 \u043e\u0442\u043a\u043b\u043e\u043d\u0435\u043d\u0438\u044f',
}

function formatDate(value) {
  if (!value) return ''

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value

  return new Intl.DateTimeFormat('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  }).format(date)
}

function mapBoard(board) {
  return {
    id: board.id,
    title: board.title,
    description: board.description,
    context: board.description || '',
    role: board.role || 'member',
    allowAnonymous: board.anon_ideas ?? true,
    autoApprove: board.moderation === undefined ? false : !board.moderation,
    members: board.members || [],
    createdAt: formatDate(board.created_at),
  }
}

function mapIdea(idea, boardId) {
  return {
    id: idea.id,
    boardId: idea.id_board || idea.board_id || boardId,
    title: idea.title,
    description: idea.description,
    status: idea.status,
    isAnonymous: idea.is_anonymous ?? false,
    author: idea.is_anonymous ? text.anonymous : text.member,
    createdAt: formatDate(idea.created_at),
    votesYes: idea.votesYes || 0,
    votesNo: idea.votesNo || 0,
    rejectionReason: idea.rejectionReason || '',
  }
}

function setError(error) {
  state.error = error?.message || text.requestError
}

export function useAppStore() {
  async function requestLogin(email) {
    state.error = ''
    state.loading = true

    try {
      const data = await authApi.login(email)
      return data.exists
    } catch (error) {
      setError(error)
      throw error
    } finally {
      state.loading = false
    }
  }

  async function registerUser(payload) {
    state.error = ''
    state.loading = true

    try {
      await authApi.register(payload)
    } catch (error) {
      setError(error)
      throw error
    } finally {
      state.loading = false
    }
  }

  async function verifyLogin({ email, code }) {
    state.error = ''
    state.loading = true

    try {
      const data = await authApi.verify({ email, code })
      state.auth.user = data.user
      state.auth.accessToken = data.access_token
      state.auth.refreshToken = data.refresh_token
      saveTokens({ accessToken: data.access_token, refreshToken: data.refresh_token })
      setAccessToken(data.access_token)
      await loadBoards()
    } catch (error) {
      setError(error)
      throw error
    } finally {
      state.loading = false
    }
  }

  async function checkUsername(username) {
    const data = await usersApi.checkUsername(username)
    return data.available
  }

  function logout() {
    clearTokens()
    setAccessToken('')
    state.auth.user = null
    state.auth.accessToken = ''
    state.auth.refreshToken = ''
    state.boards = []
    state.ideas = []
  }

  async function loadBoards() {
    const data = await boardsApi.getBoards()
    state.boards = data.items.map(mapBoard)
    return state.boards
  }

  async function createBoard(payload) {
    const data = await boardsApi.createBoard({
      title: payload.title,
      description: payload.description,
      moderation: payload.moderation ?? !payload.autoApprove,
      anon_ideas: payload.anon_ideas ?? payload.allowAnonymous ?? true,
    })

    const board = mapBoard({ ...data, role: 'admin' })
    state.boards.unshift(board)
    return board
  }

  async function loadBoard(boardId) {
    const data = await boardsApi.getBoard(boardId)
    const board = mapBoard(data)
    const ideas = (data.ideas || []).map((idea) => mapIdea(idea, board.id))

    state.boards = [board, ...state.boards.filter((item) => item.id !== board.id)]
    state.ideas = [...state.ideas.filter((idea) => idea.boardId !== board.id), ...ideas]

    return board
  }

  function updateBoard(boardId, payload) {
    notReady('PATCH /api/v1/boards/{board_id}')

    const board = getBoard(boardId)
    if (!board) return

    Object.assign(board, payload)
  }

  function deleteBoard(boardId) {
    notReady('DELETE /api/v1/boards/{board_id}')
    state.boards = state.boards.filter((board) => board.id !== boardId)
    state.ideas = state.ideas.filter((idea) => idea.boardId !== boardId)
  }

  function getBoard(boardId) {
    return state.boards.find((board) => board.id === boardId)
  }

  async function loadIdeas(boardId) {
    const data = await ideasApi.getBoardIdeas(boardId)
    const ideas = data.items.map((idea) => mapIdea(idea, boardId))

    state.ideas = [...state.ideas.filter((idea) => idea.boardId !== boardId), ...ideas]
    return ideas
  }

  function getBoardIdeas(boardId) {
    return state.ideas.filter((idea) => idea.boardId === boardId)
  }

  async function createIdea(boardId, payload) {
    const data = await ideasApi.createIdea({
      id_board: boardId,
      title: payload.title,
      description: payload.description,
      is_anonymous: payload.isAnonymous,
    })

    const idea = mapIdea(data, boardId)
    state.ideas.unshift(idea)
    return idea
  }

  function deleteIdea(ideaId) {
    notReady('DELETE /api/v1/ideas/{idea_id}')
    state.ideas = state.ideas.filter((idea) => idea.id !== ideaId)
  }

  function approveIdea(ideaId) {
    notReady('PATCH /api/v1/ideas/{idea_id}/status')
    const idea = state.ideas.find((item) => item.id === ideaId)
    if (!idea) return
    idea.status = 'approved'
    idea.rejectionReason = ''
  }

  function rejectIdea(ideaId, reason) {
    notReady('PATCH /api/v1/ideas/{idea_id}/status')
    const idea = state.ideas.find((item) => item.id === ideaId)
    if (!idea) return
    idea.status = 'rejected'
    idea.rejectionReason = reason || text.rejectReason
  }

  function voteIdea(ideaId, type) {
    notReady('POST /api/v1/votes')
    const idea = state.ideas.find((item) => item.id === ideaId)
    if (!idea) return
    if (type === 'yes') idea.votesYes += 1
    if (type === 'no') idea.votesNo += 1
  }

  function addMember(boardId, name) {
    notReady('POST /api/v1/boards/{board_id}/members')
    const board = getBoard(boardId)
    if (!board || !name?.trim()) return
    board.members.push({ id: Date.now(), name: name.trim(), role: 'member' })
  }

  function removeMember(boardId, memberId) {
    notReady('DELETE /api/v1/boards/{board_id}/members/{user_id}')
    const board = getBoard(boardId)
    if (!board) return
    board.members = board.members.filter((item) => item.id !== memberId)
  }

  function toggleModerator(boardId, memberId) {
    notReady('PATCH /api/v1/boards/{board_id}/members/{user_id}/role')
    const member = getBoard(boardId)?.members.find((item) => item.id === memberId)
    if (!member || member.role === 'admin') return
    member.role = member.role === 'moderator' ? 'member' : 'moderator'
  }

  function transferAdmin(boardId, memberId) {
    notReady('PATCH /api/v1/boards/{board_id}/members/{user_id}/role')
    const board = getBoard(boardId)
    if (!board) return
    board.members = board.members.map((member) => ({
      ...member,
      role: member.id === memberId ? 'admin' : member.role === 'admin' ? 'member' : member.role,
    }))
  }

  function getVoteResults(boardId) {
    return getBoardIdeas(boardId)
      .filter((idea) => idea.status === 'approved')
      .map((idea) => {
        const total = idea.votesYes + idea.votesNo
        return { ...idea, approvalPercent: total ? Math.round((idea.votesYes / total) * 100) : 0 }
      })
  }

  return {
    state,
    boards: computed(() => state.boards),
    requestLogin,
    registerUser,
    verifyLogin,
    checkUsername,
    logout,
    loadBoards,
    createBoard,
    loadBoard,
    updateBoard,
    deleteBoard,
    getBoard,
    loadIdeas,
    getBoardIdeas,
    createIdea,
    deleteIdea,
    approveIdea,
    rejectIdea,
    voteIdea,
    addMember,
    removeMember,
    toggleModerator,
    transferAdmin,
    getVoteResults,
  }
}
